from bs4 import BeautifulSoup
import requests

#grabbing data
resp = requests.get("https://iac.gatech.edu/people/faculty")

#SOUP
soup = BeautifulSoup(resp.content, "html.parser")

for elem in soup.find_all("li"):
    print(elem.prettify())