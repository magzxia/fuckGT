from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]


resp = requests.get("https://biosciences.gatech.edu/people?field_last_name_value=&field_job_category_tid=All")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(lambda tag: tag.name == "tr"):
    person = Person()
    nameStr = ""
    for name_data in elem.find_all(filter("td", "class", "views-field-field-first-name")):
        person.name = name_data.text
        nameStr += person.name
    for name_data in elem.find_all(filter("td", "class", "views-field-field-last-name")):
        person.name = name_data.text
        nameStr += person.name
    for title_data in elem.find_all(filter("td", "class", "views-field-field-title")):
        person.title = title_data.text
    if person.title == "Graduate Student":
        continue
    person.name = nameStr 
    people.append(person.__dict__)

print(tabulate(people, tablefmt="grid"))
