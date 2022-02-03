from textwrap import indent
from turtle import title
import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.websklad.biz.ua/?product=lazernyj-proektor-star-master-zvezdnoe-nebo'
response = requests.get(url, headers={
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
 })
soup = BeautifulSoup(response.text, 'lxml')
titles = soup.find("h1", class_ = "product_title entry-title")
desk = soup.find("div", class_ = "woocommerce-Tabs-panel--description")
p_desk = desk.find_all('p')
desk = ''
for p in p_desk:
    desk += p.text + "\n"
price = soup.find("span", class_ = "woocommerce-Price-amount")
with open("items.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file)    
data.update({titles.text : {"describe" : desk}})
print(data)
with open("items.json", "w", encoding="utf-8") as write_file:
    json.dump(data, 
    write_file,
    indent = 4,
    ensure_ascii=False)   
# print(titles.text)
# print(desk)