from bs4 import BeautifulSoup
import bs4
import requests
from tabulate import tabulate

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

#Getting all the faculty members
people: list[Person] = []
for elem in soup.find_all(li_filter):
    person = Person()
    for name_raw in elem.find_all(name_filter):
        person.name = name_raw.text

    for title_raw in elem.find_all(title_filter):
        person.title = title_raw.text.replace("Title: ", "")
    
    for home_unit_raw in elem.find_all(home_unit_filter):
        person.home_unit = home_unit_raw.text.replace("Home Unit: ", "")
        
    people.append(person)

#filtering by home_unit
center_adv_coms = []
economics = []
hist_soc = []
intl_affairs = []
literature = []
modern_languages = []
public_policy = []

for person in people:
    if person.home_unit == "Center for Advanced Communications Policy":
        center_adv_coms.append(person.__dict__)
    elif person.home_unit == "School of Economics":
        economics.append(person.__dict__)
    elif person.home_unit == "School of History and Sociology":
        hist_soc.append(person.__dict__)
    elif person.home_unit == "School of International Affairs":
        intl_affairs.append(person.__dict__)
    elif person.home_unit == "School of Literature, Media, and Communication":
        literature.append(person.__dict__)
    elif person.home_unit == "School of Modern Languages":
        modern_languages.append(person.__dict__)
    else:
        public_policy.append(person.__dict__)

print(tabulate(center_adv_coms))
print(tabulate(economics))
print(tabulate(hist_soc))
print(tabulate(intl_affairs))
print(tabulate(literature))
print(tabulate(modern_languages))
print(tabulate(public_policy))