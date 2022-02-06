from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

class Person:
    def __init__(self, name="", title=""):
        self.name = name
        self.title = title

def filter(element, attr, search):
    return lambda tag: tag.name == element and attr in tag.attrs and search in tag[attr]

def wrap(string: str):
    limit = int(len(string)/3)
    return string[:limit] + "\n" + string[limit:limit*2] + "\n" + string[(limit*2):]


def req(pages) -> list:
    lst = []
    for i in range(pages):
        resp = requests.get(f"https://www.me.gatech.edu/staff/all?field_last_name_value=&field_staff_group_target_id=All&field_all_research_areas_target_id=All&page={i}")
        soup = BeautifulSoup(resp.content, "html.parser")

        for elem in soup.find_all(filter("div", "class", "faculty__user-details")):
            person = Person()
            for name_data in elem.find_all(filter("div", "class", "faculty-name")):
                person.name = name_data.text.strip()
            for title_data in elem.find_all(filter("div", "class", "faculty-title")):
                if len(title_data.text) > 100:
                    person.title = wrap(title_data.text)
            break
        person.title = title_data.text.strip()

        lst.append(person.__dict__)
        return lst


people = req(12)
print(tabulate(people, tablefmt="grid"))