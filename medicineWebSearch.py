from bs4 import BeautifulSoup
import requests
import difflib
import re

drug_to_search = "apap"
drug_to_search_id = 1

def find_alternative_in_baza_lekow(drug_to_search, drug_to_search_id):
    link = 'https://baza-lekow.com.pl/?s={drug}'.format(drug = drug_to_search)
    page_baza_lekow = requests.get(link)
    soup = BeautifulSoup(page_baza_lekow.content, 'html.parser')
    not_found = soup.find('div',{"class":"no-results not-found"})
    if not_found is not None:
        print("drug not found")
        return "drug not found"
    else:
        links = soup.select('a')
        page_to_scrape = ""
        for link in links:
            text = link.text
            text = text.strip() if text is not None else ''
            if text.lower() == drug_to_search.lower():
                href = link.get('href')
                href = href if href is not None else ''
                page_to_scrape = href
                print(text, href)
        page_url = requests.get(page_to_scrape)
        soup2 = BeautifulSoup(page_url.text, 'html.parser')
        links = soup2.select('a')
        active_substance = None
        for link in links:
            href = link.get('href')
            if href is not None and "substancja-czynna" in href:
                active_substance = href
        if active_substance is None:
            print("no alternatives found")
            return "no alternatives found"
        substance_url = requests.get(active_substance)
        soup3 = BeautifulSoup(substance_url.text, 'html.parser')
        links = soup3.select('a')
        links_to_save= set()
        for link in links:
            href = link.get('href')
            if href is not None and "lek-ulotka" in href:
                links_to_save.add(href)
        print(links_to_save)
        return(links_to_save)

def find_alternative_in_osoz(drug_to_search):
    url = 'https://www.osoz.pl/osoz-www/leki/tanszeZamienniki/szukaj'
    data = {'searchInput': f'{drug_to_search}'}
    page_to_find_drug = requests.post(url, data)
    soup = BeautifulSoup(page_to_find_drug.content, 'html.parser')
    div = soup.find('div', {"id": "items_posts"})
    first_outcome = div.find('h5', {"class": "toogle-lista-lekow"})
    onclick = first_outcome.get('onclick')
    id = onclick.split(",")[4].split()[0]
    name = onclick.split(",")[2].split("'")[1]
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    searchData = {"searchAjax":
        "{" +
            "'nazwa': '" + name + "'," +
            "'nazwaWyswietlana': '" + name + "'," +
            "'id': '" + id + "'," +
            "'typ':'BRAND'," +
            "'typNad':''" +
        "}"
    }
    page_osoz = requests.post('https://www.osoz.pl/osoz-www/leki/szukaj/znajdzElementyAjax', searchData, header)

    first_link = re.search("\/osoz-www\/leki\/szczegoly\/[0-9]*", page_osoz.text).group();
    id = first_link.rsplit("/")[4]
    page_with_alternative = requests.get('https://www.osoz.pl/osoz-www/leki/tanszeZamienniki/' + id)
    soup = BeautifulSoup(page_with_alternative.content, 'html.parser')

    main_text = soup.find('div', {'class': 'full-text'})
    if main_text is None:
        return "no alternatives"
    alternatives = main_text.find('table', {"class": "price-table"}).findAll('a')

    for link in alternatives:
        alternative_json = dict()
        name =link.text.strip().replace(" ", "-")
        alternative_json['name'] = name
        url_link = f"https://baza-lekow.com.pl/{name}-lek-ulotka-chpl-opinie-dawkowanie/"
        if find_description(url_link) is not None:
            alternative_json['url_link'] = url_link
            alternative_json['description'] = find_description(url_link)
            alternative_json['is_antibiotic'] = find_is_antibiotic(url_link)
            alternative_json['is_steroid'] = find_is_steroid(url_link)
            alternative_json['is_prescription_needed'] = find_is_prescription_drug(link.get('href'))
        print(alternative_json)



def find_is_antibiotic(url_link):
    url_page = requests.get(url_link)
    soup = BeautifulSoup(url_page.content, 'html.parser')
    paragraph_connected_categories = soup.find('div', {"class": "code-block code-block-13"})
    links = paragraph_connected_categories.select('a')
    for link in links:
        if link.text.strip() == "Antybiotyki":
            return True
    return False


def find_is_steroid(url_link):
    url_page = requests.get(url_link)
    soup = BeautifulSoup(url_page.content, 'html.parser')
    if soup.text.find("steroid") is not -1 and soup.text.find("niesteroid") is -1:
        return True
    else:
        return False


def url_prepare(drug):
    return drug.strip().replace(" ", "-")


def find_is_prescription_drug(url_link_ktomalek):
    url_page = requests.get(url_link_ktomalek)
    soup = BeautifulSoup(url_page.content, 'html.parser')
    paragraph = soup.find('p', {"class": "m:t:l"}).find('a')
    if paragraph.text == "lek na receptę":
        return True
    elif paragraph.text == "lek dostępny bez recepty":
        return False

def find_description(url_link):
    url_page = requests.get(url_link)
    soup = BeautifulSoup(url_page.content, 'html.parser')
    paragraph = soup.find('div', {"id": "page"}).find('div', {"class": "entry-content", "itemprop": "text"}).find('p')
    if paragraph.text.startswith("Witaj"):
        return None
    else:
        return paragraph.text



drug = "apap"
name = drug.strip().replace(" ", "-")
url_link = f"https://baza-lekow.com.pl/{name}-lek-ulotka-chpl-opinie-dawkowanie/"
# url_link ="https://ktomalek.pl/l/ulotka/sastium-tabl-powl-0-05-g-28-tabl/b-3194023"
# url_link = "https://ktomalek.pl/apap-caps-ulotka-cena-zastosowanie-apteka-kapsulki-miekkie-0-5-g-10-kaps/ub-3251446"
# print(url_link)
find_alternative_in_osoz(drug)





