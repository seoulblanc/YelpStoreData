
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

req = requests.get("https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY") # start=30 붙이면 다음 페이지
html = req.text

soup = BeautifulSoup(html, 'html.parser')
name_class = soup.findAll("a", {"class":"biz-name js-analytics-click"})
list_name = []
for i in name_class :
    name = i.find("span").text
    list_name.append(name)
#print(list_name)

list_category = []
category_class = soup.findAll("span", {"class":"category-str-list"}) #여러개
for k in category_class :
    sub_list = []
    category = k.findAll("a")
    for m in category :
        one_ca = m.text
        sub_list.append(one_ca)
    list_category.append(sub_list)
#print(list_category)


comment_class = soup.findAll("p", {"class":"snippet"})
list_comment = []
for n in comment_class :
    nn = n.text
    print(nn)
    nnn = re.findall(r'\w+', nn)
    list_comment.append(nnn)
    \

#print(list_comment)

df = pd.DataFrame(
    {'store' : list_name,
    'category' : list_category,
    'comment' : list_comment,
    })

print(df)
