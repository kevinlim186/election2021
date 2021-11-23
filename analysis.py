from pymysql.connections import lenenc_int
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from src.database import Database


database = Database()

texts=database.get_texts()

texts['_text'] =texts['_text'].str.replace('\n', ' ') #replace next line with space
texts = texts[~texts['_text'].isna()]


bbm= " ".join(texts[texts['group_candidate']=='Marcos-Duterte']['_text'].values)
leni= " ".join(texts[texts['group_candidate']=='Leni-Kiko']['_text'].values)
isko= " ".join(texts[texts['group_candidate']=='Isko-Ong']['_text'].values)

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(isko)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()