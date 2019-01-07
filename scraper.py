import requests
import pandas
from bs4 import BeautifulSoup

page_url = "https://inlandempire.craigslist.org/search/sss?sort=rel&query=wii"
page_response = requests.get(page_url, timeout=5)
soup = BeautifulSoup(page_response.content, "html.parser")
print(soup.prettify())
