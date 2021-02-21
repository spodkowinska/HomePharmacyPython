from bs4 import BeautifulSoup
import requests
import difflib
import re

drug_to_search = "zotral"


def find_alternative_in_baza_lekow(drug_to_search):
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
    print(searchData)
    page_osoz = requests.post('https://www.osoz.pl/osoz-www/leki/szukaj/znajdzElementyAjax', searchData, header)
    # print(page_osoz.text)

    first_link = re.search("\/osoz-www\/leki\/szczegoly\/[0-9]*", page_osoz.text).group();
    id = first_link.rsplit("/")[4]
    print(id)
    page_with_alternative = requests.get('https://www.osoz.pl/osoz-www/leki/tanszeZamienniki/' + id)
    soup = BeautifulSoup(page_with_alternative.content, 'html.parser')

    alternatives = soup.find('div', {'class': 'full-text'}).find('table', {"class": "price-table"}).findAll('a')
    for link in alternatives:
         print(link)


    f"https://baza-lekow.com.pl/{name}-lek-ulotka-chpl-opinie-dawkowanie/"

        # page_to_scrape = ""
        # for link in links:
        #     text = link.text
        #     text = text.strip() if text is not None else ''
        #     if text.lower() == drug_to_search.lower():
        #         href = link.get('href')
        #         href = href if href is not None else ''
        #         page_to_scrape = href
        #         print(text, href)
        # page_url = requests.get(page_to_scrape)
        # soup2 = BeautifulSoup(page_url.text, 'html.parser')
        # links = soup2.select('a')
        # active_substance = None
        # for link in links:
        #     href = link.get('href')
        #     if href is not None and "substancja-czynna" in href:
        #         active_substance = href
        # if active_substance is None:
        #     print("no alternatives found")
        #     return "no alternatives found"
        # substance_url = requests.get(active_substance)
        # soup3 = BeautifulSoup(substance_url.text, 'html.parser')
        # links = soup3.select('a')
        # links_to_save= set()
        # for link in links:
        #     href = link.get('href')
        #     if href is not None and "lek-ulotka" in href:
        #         name = link.text
        #         name = name.strip() if name is not None else ''
        #         links_to_save.add(href)
        # print(links_to_save)
        # return(links_to_save)

# find_alternative_in_baza_lekow(drug_to_search)
find_alternative_in_osoz(drug_to_search)







