from bs4 import BeautifulSoup
import requests
import csv

class Person:
    def __init__(self, name="", title=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]

def wrap(string: str):
    limit = int(len(string)/3)
    return string[:limit] + "\n" + string[limit:limit*2] + "\n" + string[(limit*2):]



resp = requests.get("https://chbe.gatech.edu/people?title=&field_disciplines_tid=All&field_work_group_tid=3")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(filter("div", "class", "views-row")):
    person = Person()
    for name_data in elem.find_all(filter("a", "href", "/people/")):
        if "View Full Profile" in name_data.text:
            continue
        person.name = name_data.text
    
    for title_data in elem.find_all(filter("div", "class", "views-field-field-job-title")):
        if len(title_data.text) > 100:
            person.title = wrap(title_data.text)
            break
        person.title = title_data.text 
    
    people.append(person.__dict__)
