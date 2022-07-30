from itertools import count
from re import L
import unicodedata
import requests
from bs4 import BeautifulSoup
import json

yandex_url = "https://yandex.ru"
locations_url = "/jobs/locations/"
massiv = {}

p = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
    "Cookie": "_yasc=U5Mtr0YYQtXlZDH7qJ8yK3j/3jlhLdxoS1uTZN+XgKGJ14JTqDw=; _ym_isad=2; _ym_d=1659003453; _ym_uid=1658832458444206493; gdpr=0; yandexuid=3871665821658832453; ymex=1690368458.yrts.1658832458; yp=1659437255.szm.2:1440x900:1440x737; i=HuNllhtbEh7Pp1LQGgefnEv2e/rukzwfqJOJ85T75MMcr1RL9z8WzIROP5swGtndujCUa8680Wpgc8ZvY41tEYkNQyY=; is_gdpr=1; is_gdpr_b=CLryEBDFgAEYAQ=="
}

URL = yandex_url + locations_url

def parser(u):

    s = requests.session()
    r = s.get(u, params=p)
    soup = BeautifulSoup(r.text, "html.parser")

    return soup


def getstrani():

    soup = parser(URL)

    div = soup.find_all("h3", class_="lc-styled-text__text")

    strani = []

    i = 1
    for element in div:
        strani.append(element.get_text())

    strani.pop(-1)
    strani.pop(-1)

    strani.reverse()

    strani.pop(-1)
    strani.pop(-1)

    return strani


def getlinks():

    soup = parser(URL)

    mass = soup.find_all("a", class_="Link link lc-link")

    mass.reverse()

    links = list()

    for m in mass:
        links.append(m.get("href"))
    
    return links




def getgoroda():

    soup = parser(URL)

    mass = soup.find_all("div", class_="lc-jobs-text lc-jobs-text_type_header lc-jobs-text_size_s lc-jobs-text_isInline lc-jobs-entity-list__item-title-text")

    mass.reverse()

    goroda = list()

    for m in mass:
        goroda.append(m.get_text())
        if m.get_text() == "Минск":
            break
    
    goroda.pop(-1)

    return goroda



def getcount():

    soup = parser(URL)
    mass = soup.find_all("div", class_="lc-jobs-text lc-jobs-text_type_text lc-jobs-text_size_s lc-jobs-text_isInline lc-jobs-entity-list__item-title-badge")
    mass.reverse()

    count = list()

    for c in mass:
        count.append(c.get_text())
    
    return count



def vacancy(u):
    soup = parser(u)
    text = "lc-jobs-text lc-jobs-text_type_header lc-jobs-text_size_s lc-jobs-vacancy-card__header"
    search = soup.find_all("div", class_=text)

    vac = list()
    for s in search:
        vac.append(s.get_text())

    return vac






def sozdaniemassiva():
    strani = getstrani()
    goroda = getgoroda()
    count = getcount()
    links = getlinks()

    v = dict()

    for l in range(0, len(strani)):
        v[l] = vacancy(yandex_url + links[l])
        
    for i in range(0, len(strani)):
        massiv[strani[i]] = goroda[i], count[i], links[i], ({"Вакансии": v[i]})




    with open("yandexjobs.json", "w") as file:
        json.dump(massiv, file, indent=4, ensure_ascii=False)




if __name__ == "__main__":
    sozdaniemassiva()




