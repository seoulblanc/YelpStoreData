import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def request_url():
    URL1 = "http://www.weather.go.kr/weather/climate/past_cal.jsp?stn=108&yy="
    URL2 = "&mm="
    URL3 = "&obs=1&x=35&y=13"
    URL = URL1 + year + URL2 + month + URL3

    try:
        print(URL)
        req = requests.get(URL)
        html = req.text
        return html

    except Exception as e:
        print(e)
        print("Error for URL")
        pass

def get_data():
    html = request_url()
    soup = BeautifulSoup(html, 'html.parser')
    selected_class = soup.findAll("option", {"selected":"selected"})
    weather_class = soup.findAll("td", {"class": "align_left"})

    date = []
    weather = []
    value01 = []
    value02 = []
    value03 = []
    value04 = []
    value05 = []

    for i in weather_class :
        each = i.text
        if len(each) < 5 and each != '\xa0':
            date.append(each)
        if len(each) > 5 :
            weather.append(each)
            p = re.compile('[\d+-.]+')
            passer = p.findall(each)
            value01.append(passer[0])
            value02.append(passer[1])
            value03.append(passer[2])
            value04.append(passer[3])
            value05.append(passer[4])

    df = pd.DataFrame(
        {'year' : ['%s' %(year)] * len(date),
        'month' : ['%s' %(month)] * len(date),
        'date' : date,
        '평균기온' : value01,
        '최고기온': value02,
        '최저기온': value03,
        '평균운량' : value04,
        '일강수량' : value05,
        })
    # print(df)
    return df

if __name__ == "__main__":
    year = '2017'
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    columns = ['year', 'month', 'date', '평균기온', '최고기온', '최저기온', '평균운량', '일강수량']
    alldf = pd.DataFrame(columns=columns)

    for month in months :
        month = str(month)
        df = get_data()
        alldf = pd.concat([alldf, df])

    print(alldf)
    alldf.to_csv("c:/pythondata/weather2017.csv", header=True, index=False)

