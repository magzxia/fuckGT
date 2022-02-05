from bs4 import BeautifulSoup
import bs4
import requests

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title
        self.home_unit = home_unit

#grabbing data
resp = requests.get("https://iac.gatech.edu/people/faculty")

#SOUP
soup = BeautifulSoup(resp.content, "html.parser")

#Filter functions
def li_filter(tag: bs4.Tag) -> bool:
    if tag.name == "li" and "id" in tag.attrs:
        return "iac-person" in tag["id"]
    else:
        return False

def name_filter(tag:bs4.Tag) -> bool:
    if tag.name == "a" and "href" in tag.attrs:
        return "/people/person" in tag["href"]
    else:
        return False

def title_filter(tag:bs4.Tag) -> bool:
    if tag.name == "p" and "class" in tag.attrs:
        return "iacPersonTitle" in tag["class"]
    else:
        return False

def home_unit_filter(tag:bs4.Tag) -> bool:
    if tag.name == "p" and "class" in tag.attrs:
        return "iacPersonHomeUnit" in tag["class"]
    else:
        return False

people = []
for elem in soup.find_all(li_filter):
    person = Person()
    for name_raw in elem.find_all(name_filter):
        person.name = name_raw.text

    for title_raw in elem.find_all(title_filter):
        person.title = title_raw.text
    
    for home_unit_raw in elem.find_all(home_unit_filter):
        person.home_unit = home_unit_raw.text
        
    people.append(person)

for person in people:
    print(person.__dict__)