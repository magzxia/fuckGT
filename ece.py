from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]


resp = requests.get("https://www.ece.gatech.edu/faculty-staff-directory?field_group_filter_value=1")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(filter("div", "class", "faculty-staff-information")):
    person = Person()
    for name_data in elem.find_all(filter("div", "class", "field-full-name")):
        person.name = name_data.text
    for title_data in elem.find_all(filter("div", "class", "field-jobtitle")):
        person.title = title_data.text
    people.append(person.__dict__)

print(tabulate(people, tablefmt="grid"))