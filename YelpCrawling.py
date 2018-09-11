#yelp crawling (use this one)

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


def get_one_store():
    html = request_url()
    soup = BeautifulSoup(html, 'html.parser')
    find_one_store = soup.findAll("li", {"class": "regular-search-result"})
    one_store_info = []

    for j in find_one_store:
        sub_store_info = []

        i = j.findAll("a", {"class": "biz-name js-analytics-click"})
        for one in i :
            name = one.find("span").text
            sub_store_info.append(name)
            # print(name)

        k = j.findAll("span", {"class": "category-str-list"})
        for one in k :
            category = one.find("a").text
            sub_store_info.append(category)
            # print(category)

        n = j.findAll("p", {"class": "snippet"})
        for one in n:
            n_text = one.text
            n_text = re.findall(r'\w+ ', n_text)
            sub_store_info.append(n_text)
            # print(n_text)

        if len(sub_store_info) == 3 :
            one_store_info.append(sub_store_info)
        else :
            pass

    return one_store_info

def save_csv():
    alldf.to_csv("/Users/yoon/Documents/Yelp_NewYork_30.csv" , header=True, index=False)

if __name__ == "__main__":
    alldf = pd.DataFrame(columns=('store', 'category','comment'))
    for i in range(0, 30):
        URL2 = "%s" % (i * 30)
        one_store_info = get_one_store()
        pd30 = pd.DataFrame(one_store_info, columns=('store','category','comment') )
        alldf = pd.concat([alldf, pd30], 0)

    #print(alldf)
    save_csv()
    print('Done')



