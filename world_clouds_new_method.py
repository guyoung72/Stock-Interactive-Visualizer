import requests
import urllib.request
import time
import spacy
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

#구글 서치
keyword=input('Type keyword:')
whatnumber=int(input("How many search results do you want to scrap? (100 is the default value):") or "100")
topic=keyword
numResults=whatnumber
url ="https://www.google.com/search?q="+topic+"&tbm=nws&hl=en&num="+str(numResults)
response = requests.get(url)
#수프 html parser로 하기 (가끔 딴걸로 해야됨)
soup = BeautifulSoup(response.content, 'html.parser')
results = soup.find_all('div', attrs = {'class': 'ZINbbc'})
descriptions = []

#s3v9rd마다 분류해서 끊기
for result in results:
    try:
        description = result.find('div', attrs={'class':'s3v9rd'}).get_text()
        if description != '':
            descriptions.append(description)
    except:
        continue
text = ''.join(descriptions)

#spacy english
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
newText =''

#stop_words 계속 add하기
stop_words = ["will","announced","announces","launched","launches","inch","year","size","best","analysis","greetings","business","exit","now","today","according","feature","including","says","pick","report","say","said","official","offer","people","spoke","day","week","hour","month","days","hours"]\
             +list(STOPWORDS)

for word in doc:
 if word.pos_ in ['ADJ', 'NOUN']:
  newText = " ".join((newText, word.text.lower()))
wordcloud = WordCloud(stopwords=stop_words).generate(newText)

#visualize
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()