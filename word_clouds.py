import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# #change it to input format after finishing making the whole webscraper
# page=urllib.request.urlopen("https://www.webull.com/newslist/nasdaq-msft")
# # page=urllib.request.urlopen("https://www.investing.com/equities/microsoft-corp-commentary")
# soup=bs(page,"html.parser")
#
# names=soup.body.findAll('div')
# function_names=re.findall('wbus14.\w+',str(names))
#
# print(names)

mostActiveStocksUrl = "https://www.nasdaq.com/market-activity/most-active"
r = requests.get(mostActiveStocksUrl)
data = r.text
soup = BeautifulSoup(data)

table = soup.find_all('div', attrs="class"&"genTable")
all_rows = table[1].find_all('tr')

symbols = []
names = []
last_sales = []
change_nets = []
share_volumes = []

for row in all_rows:
    cols=row.find_all('td')
    if(len(cols)):
        names.append(cols[1].text)
        last_sales.append(cols[2].text)
        change_nets.append(cols[3].text)
        share_volumes.append(cols[4].text)

data=pd.DataFrame({&quot;Names&quot;:names,&quot;Last Sale&quot;: last_sales,&quot;Chnange Net&quot;: change_nets,&quot;Share Volume&quot;: share_volumes})
