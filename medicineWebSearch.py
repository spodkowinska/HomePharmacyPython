from bs4 import BeautifulSoup
import requests
drug_to_search = "zotral"
link = 'https://baza-lekow.com.pl/?s={drug}'.format(drug = drug_to_search)
page_baza_lekow = requests.get(link)
soup = BeautifulSoup(page_baza_lekow.content, 'html.parser')
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
active_substance = ""
for link in links:
    href = link.get('href')
    if href is not None and "substancja-czynna" in href:
        active_substance = href

substance_url = requests.get(active_substance)
soup3 = BeautifulSoup(substance_url.text, 'html.parser')
links = soup3.select('a')
links_to_save= set()
for link in links:
    href = link.get('href')
    if href is not None and "lek-ulotka" in href:
        name = link.text
        name = name.strip() if name is not None else ''
        alternative = name, href
        links_to_save.add(href)
print(links_to_save)







