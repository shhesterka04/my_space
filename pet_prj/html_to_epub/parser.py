import requests
from bs4 import BeautifulSoup
r = requests.get('https://2top.notion.site/5-2022-09fd029f28e94fa9811b8cb9bbe2f317')
r = r.text
soup = BeautifulSoup(r, 'lxml')

print(soup.title.text)
