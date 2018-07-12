
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL1 = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start="

def request_url():
    try:
        for i in range(0,1000):
            URL2 = "%s" %(i*30)
            URL = URL1 + URL2
            req = requests.get(URL)
            html = req.text
            print(html)
            return html
    except Exception as e:
        print(e)
        print("Error for URL")

def get_data(html):
    # 매장 이름 가지고 오기
    soup = BeautifulSoup(html, 'html.parser')
    name_class = soup.findAll("a", {"class":"biz-name js-analytics-click"})
    list_name = []
    for i in name_class :
        name = i.find("span").text
        list_name.append(name)
    #print(list_name)

    # 매장 카테고리 가지고 오기
    list_category = []
    category_class = soup.findAll("span", {"class":"category-str-list"})
    for k in category_class :
        sub_list = []
        category = k.findAll("a")
        for m in category :
            one_ca = m.text
            sub_list.append(one_ca)
        list_category.append(sub_list)
    #print(list_category)

    # 매장 댓글 가지고 오기
    comment_class = soup.findAll("p", {"class":"snippet"})
    list_comment = []
    for n in comment_class :
        nn = n.text
        nnn = re.findall(r'\w+ ', nn)
        list_comment.append(nnn)
    #print(list_comment)

    return list_comment, list_category, list_name

def make_dataframe(list_comment,list_category,list_name):
    df = pd.DataFrame(
        {'comment' : list_comment,
         'category': list_category,
         'store' : list_name,
        })
    df['category'] = df['category'].str[0]
    # df['comment'] = df['comment'].str.strip('[]')
    return df

def gather_df(df):
    pass

def save_csv(all_df):
    pass
    # all_df.to_csv("c:/pythondata/Yepl_Test02.csv", header=True, index=False)

