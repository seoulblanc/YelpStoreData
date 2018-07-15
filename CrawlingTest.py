# Yelp 크롤링 by columns

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def request_url():
    URL1 = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=New+York,+NY&start="
    try:
        URL = URL1 + URL2
        print(URL)
        req = requests.get(URL)
        html = req.text
        return html

    except Exception as e:
        print(e)
        print("Error for URL")


def get_data():
    html = request_url()
    # 매장 이름 가지고 오기
    soup = BeautifulSoup(html, 'html.parser')
    name_class = soup.findAll("a", {"class": "biz-name js-analytics-click"})
    list_name = []
    for i in name_class:
        name = i.find("span").text
        list_name.append(name)
    # print(list_name)

    # 매장 카테고리 가지고 오기
    list_category = []
    category_class = soup.findAll("span", {"class": "category-str-list"})
    for k in category_class:
        sub_list = []
        category = k.findAll("a")
        for m in category:
            one_ca = m.text
            sub_list.append(one_ca)
        list_category.append(sub_list)
    # print(list_category)

    # 매장 댓글 가지고 오기
    comment_class = soup.findAll("p", {"class": "snippet"})
    list_comment = []

    for n in comment_class:
        nn = n.text
        nnn = re.findall(r'\w+ ', nn)
        list_comment.append(nnn)

    # print(list_comment)
    return list_comment, list_category, list_name


def make_dataframe():
    list_comment, list_category, list_name = get_data()
    print(len(list_comment))
    print(len(list_category))
    print(len(list_name))

    if i == 0:
        df = pd.DataFrame(
            {'comment': list_comment[1:31],
             'category': list_category[1:31],
             'store': list_name[1:31], })
    else:
        df = pd.DataFrame(
            {'comment': list_comment[1:31],
             'category': list_category[1:31],
             'store': list_name[1:31], })
    df['category'] = df['category'].str[0]
    # df['comment'] = df['comment'].str.strip('[]')
    # print(df)
    return df

def save_csv():
    alldf.to_csv("/Users/yoon/Documents/Yepl_Test01.csv", header=True, index=False)


if __name__ == "__main__":
    alldf = pd.DataFrame(columns=('store', 'comment', 'category'))
    for i in range(0, 5):
        URL2 = "%s" % (i * 30)
        alldf = pd.concat([alldf,make_dataframe()], ignore_index=True, sort=True)
    print(alldf)
    save_csv()


