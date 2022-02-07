from bs4 import BeautifulSoup
import requests
import csv

class Person:
    def __init__(self, name="", title="", home_unit=""):
        self.name = name
        self.title = title
        self.home_unit = home_unit

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]

def wrap(string: str):
    limit = int(len(string)/3)
    return string[:limit] + "\n" + string[limit:limit*2] + "\n" + string[(limit*2):]


def req(pages, id, home) -> list:
    lst = []
    for i in range(pages):
        resp = requests.get(f"https://www.cc.gatech.edu/index.php/people/faculty?field_person_school_target_id[{id}]={id}&page={i}")
        soup = BeautifulSoup(resp.content, "html.parser")

        for elem in soup.find_all(filter("div", "class", "profile-card__content")):
            person = Person(home_unit=home)
            for name_data in elem.find_all(filter("a", "href", "/people/")):
                person.name = name_data.text
            for title_data in elem.find_all(filter("h6", "class", "card-block__subtitle")):
                person.title = title_data.text

            lst.append(person.__dict__)
    return lst

compute_inst = req(2, 321, "Division of Computing Instruction")
compute_sci_and_engineering = req(5, 203, "School of Computational Science and Engineering")
comp_sci = req(6, 204, "School of Computer Science")
cyber_sec = req(3, 292, "School of Cybersecurity and Privacy")
int_computing = req(8, 205, "School of Interactive Computing")

units = [compute_inst, compute_sci_and_engineering, comp_sci, cyber_sec, int_computing]

with open("computing.csv", "w") as file:
    fieldnames = ["name", "title", "home_unit"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for unit in units:
        for data in unit:
            print(data)
            writer.writerow(data)