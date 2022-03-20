from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

keyword=input('Type Keyword:')

root="https://www.google.com/"
link="https://www.google.com/search?q="+keyword+"&newwindow=1&tbm=nws&sxsrf=APq-WBu72XeslioaVhmBnd0zw0ThgKeD_w:1647756625505&source=lnt&tbs=qdr:w&sa=X&ved=2ahUKEwi0qdvig9T2AhXWU80KHY4eDbkQpwV6BAgBEBw&biw=1920&bih=937&dpr=1"

def news(link):
    req=Request(link,headers={'User-Agent':'Mozilla/5.0'})
    webpage=urlopen(req).read()
    with requests.Session() as c:
        soup=BeautifulSoup(webpage,'html5lib')
        # print(soup)
        for item in soup.find_all('div',attrs={'class':'ZINbbc luh4tb xpd O9g5cc uUPGi'}):
            raw_link=(item.find('a',href=True)['href'])
            link=raw_link.split("/url?q=")[1].split("&sa=U&")[0]
            # print(item)
            title=(item.find('div',attrs={'class':'BNeawe vvjwJb AP7Wnd'})).get_text()
            desc=(item.find('div',attrs={'class':'BNeawe s3v9rd AP7Wnd'})).get_text()

            title=title.replace(",","")
            title = title.replace("—", "")
            title = title.replace("–", "")

            desc=desc.replace(",", "")
            desc = desc.replace("—", "")
            desc = desc.replace("–", "")
            desc = desc.replace("£", "")
            time=desc.split("·")[0]
            descript=desc.split("·")[1]
            # print(title)
            # print(time)
            # print(descript)
            # print(link)
            document=open("data.csv","a")
            document.write("{},{},{},{} \n".format(title, time, descript, link))
            document.close()
        next=soup.find('a',attrs={'aria-label':'Next page'})
        next=(next['href'])
        link=root+next
        news(link)
news(link)
print('csv file created and written successfully')