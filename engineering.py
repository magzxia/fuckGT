from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

class Person:
    def __init__(self, name="", title=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]


resp = requests.get("https://ae.gatech.edu/people?field_lab_collaborations_tid=All&title=&field_disciplines_tid=All&field_ae_multidisciplinary_resea_tid=All&field_work_group_tid=3")
soup = BeautifulSoup(resp.content, "html.parser")

people = []
for elem in soup.find_all(filter("div", "class", "view-content")):
    person = Person()
    for name_data in elem.find_all(filter("a", "href", "/people/")):
        if name_data.text != "View Full Profile":
            person.name = name_data.text
            print (person.name)
    for title_data in elem.find_all(filter("div", "class", "field-content")):
        hasDigit = True
        for char in title_data.text:
            if char.isdigit():
                hasDigit = False
        if hasDigit and title_data.text != "":
            person.title = title_data.text 
            print(person.title)   

    people.append(person.__dict__)
print(tabulate(people, tablefmt="grid"))