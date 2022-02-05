from xmlrpc.client import Boolean
from bs4 import BeautifulSoup
import bs4
import requests

#grabbing data
resp = requests.get("https://iac.gatech.edu/people/faculty")

#SOUP
soup = BeautifulSoup(resp.content, "html.parser")

def li_filter(tag: bs4.Tag) -> Boolean:
    if tag.name == "li" and "id" in tag.attrs:
        return "iac-person" in tag["id"]
    else:
        return False 

elems = []
for elem in soup.find_all(li_filter):
    elems.append(elem)

print(elems[0].prettify())