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



resp = requests.get("https://math.gatech.edu/people?field_job_type_tid=16")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(lambda tag: tag.name == "tr"):
    person = Person()
    for name_data in elem.find_all(filter("a", "href", "/people/")):
        person.name = name_data.text.strip()
    for title_data in elem.find_all(filter("td", "class", "views-field-field-job-title")):
        if len(title_data.text) > 100:
            person.title = wrap(title_data.text)
            break
        person.title = title_data.text.strip()
    people.append(person.__dict__)

