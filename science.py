from re import L
from turtle import title
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


resp = requests.get("https://biosciences.gatech.edu/people?field_last_name_value=&field_job_category_tid=All")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(filter("li", "class", "biosci-people-cell")):
    person = Person()
    for name_data in elem.find_all(filter("span", "class", "p-name")):
        person.name = name_data.text.strip()
    for title_data in elem.find_all(filter("span", "class", "p-job-title")):
        if len(title_data.text) > 100:
            person.title = wrap(title_data.text)
            break
        person.title = title_data.text
    if person.title == "":
        continue
    people.append(person.__dict__)

print(tabulate(people, tablefmt="grid"))

