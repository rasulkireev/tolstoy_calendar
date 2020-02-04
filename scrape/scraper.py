import httpx
from bs4 import BeautifulSoup
import json

url = "http://tolstoy.ru/online/online-publicism/mysli-mudryh-ludey-na-kazhdiy-den/"
r = httpx.get(url)
soup = BeautifulSoup(r, 'html.parser')

month_ids = []
for i in range(4,16):
    string = "top_" + str(i)
    month_ids.append(string)

data = []
day_dict = {}

for month_id in month_ids:
    month_block = soup.find(id=month_id)
    month_name = month_block.find('h2').string
    
    days = []
    for i in month_block.find_all(class_="subtitle"):
        try:
            day = i.string.strip()
        except:
            day = i.span.string.strip()

        day_dict['month'] = month_name.title() 
        day_dict['day'] = day
        
        text = []
        s = i
        while True:
            s = s.find_next_sibling()
            if s and 'right' in s.attrs.get("class", []):
                try:
                    day_dict['author'] = s.string.strip()
                except:
                    break
            elif s and "subtitle" not in s.attrs.get("class", []):
                try:
                    text.append(s.string.strip())
                except:
                    continue
            else:
                break
                
        day_dict['text'] = text
        
        data.append(day_dict.copy())
        
    
with open('tolstoy-calendar.json','w',encoding='ascii') as f:
    json.dump(data,f)