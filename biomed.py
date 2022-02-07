from bs4 import BeautifulSoup
import requests
import csv

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]

def wrap(string: str):
    limit = int(len(string)/3)
    return string[:limit] + "\n" + string[limit:limit*2] + "\n" + string[(limit*2):]


resp = requests.get("https://bme.gatech.edu/bme/faculty")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(filter("div", "class", "views-col")):
    person = Person()
    for name_data in elem.find_all(filter("div", "class", "views-field-field-last-name")):
        person.name = name_data.text
    for title_data in elem.find_all(filter("div", "class", "views-field-field-title")):
        if len(title_data.text) > 100:
            person.title = wrap(title_data.text)
            break
        person.title = title_data.text
        person.title = title_data.text
    people.append(person.__dict__)

with open("biomed.csv", "w") as file:
    fields = ["name", "title"]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for person in people:
        writer.writerow(person)