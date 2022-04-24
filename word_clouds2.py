import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys, os
os.chdir(sys.path[0])

text=open('data.txt',mode='r').read()
stop_words = ["will","announced","announces","launched","launches","inch","year","size","best","analysis","greetings","business","exit","now","today","according","feature","including","says","pick","report","say","said","official","offer","people","spoke"]\
             +list(STOPWORDS)

wc=WordCloud(
    background_color='white',
    stopwords= stop_words,
    height=800,
    width=800
)

wc.generate(text)

#save it
wc.to_file('wordcloud_output.png')