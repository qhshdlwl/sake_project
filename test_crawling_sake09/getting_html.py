import requests
from bs4 import BeautifulSoup

url = 'http://sake09.com/shop/'
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, features='xml')

# print(soup.title.get_text())
# print(soup.a) # 처음 발견되는 a element
# print(soup.a.attrs) # a 의 속성
# print(soup.a['id']) # a 의 id

with open('./test_crawling_sake09/sake_page.xhtml', 'w', encoding='utf-8') as f:
    f.write(res.text)
    