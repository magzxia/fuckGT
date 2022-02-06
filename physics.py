from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]

def wrap(string: str):
    limit = int(len(string)/3)
    return string[:limit] + "\n" + string[limit:limit*2] + "\n" + string[(limit*2):]



resp = requests.get("https://physics.gatech.edu/people/directory")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(lambda tag: tag.name == "tr"):
    person = Person()
    for name_data in elem.find_all(filter("a", "href", "/user/")):
        person.name = name_data.text.strip()
    for title_data in elem.find_all(filter("td", "class", "views-field-field-profile-professional-title")):
        if len(title_data.text) > 100:
            person.title = wrap(title_data.text)
            break
        person.title = title_data.text.strip()
    if person.title == "Graduate Student" or person.title == "":
        continue
    people.append(person.__dict__)

print(tabulate(people, tablefmt="grid"))