from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title
        self.home_unit = home_unit

resp = requests.get("https://www.cc.gatech.edu/index.php/people/faculty")

soup = BeautifulSoup(resp.content, "html.parser")

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]

people = []
for elem in soup.find_all(filter("div", "class", "profile-card__content")):
    person = Person()
    for name_data in elem.find_all(filter("a", "href", "/people/")):
        person.name = name_data.text
    for title_data in elem.find_all(filter("h6", "class", "card-block__subtitle")):
        person.title = title_data.text

    print(person.__dict__)

