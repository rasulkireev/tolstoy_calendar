import httpx
from bs4 import BeautifulSoup

url = "http://tolstoy.ru/online/online-publicism/mysli-mudryh-ludey-na-kazhdiy-den/"

r = httpx.get(url)

soup = BeautifulSoup(r, 'html.parser')

name_box = soup.find('h1').text.strip()

print(name_box)