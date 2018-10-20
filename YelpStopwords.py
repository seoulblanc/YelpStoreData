import pandas as pd 
adlldf = pd.read_csv("Yelp_NewYork_30.csv") 
alldf.head()
#len(alldf)

sample = alldf[0:10]
sample

import re
p = re.compile('[\w]+')

stop = open("c:/pythondata/stopwords.txt", mode='r', encoding='utf-8')
stops = stop.readlines()
stops

stoplist = []
for i in stops :
    a = p.findall(i)
    a = ''.join(a)
    stoplist.append(a)
stoplist
stopstr = ', '.join(stoplist)
stopstr

# 여기서부터 다시 

new = []

for i in sample['comment']:
    i = str(i)
    newcm= p.findall(i)
    new.append(newcm)

newdf = pd.DataFrame(data=new)
print(newdf)
