from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from src.database import Database
from src.utility import STOP_WORDS as STOP_WORDS_SOURCE


database = Database()

texts=database.get_texts()

# texts=database.get_posts()

STOP_WORDS = r'\b(?:{})\b'.format('|'.join(STOP_WORDS_SOURCE))
VALID_CHARACTERS = r'[^A-Za-z0-9 ]+'
texts['_text'] =texts['_text'].str.lower() # lower case 

texts['_text'] = texts['_text'].str.replace(STOP_WORDS, '')
texts['_text'] = texts['_text'].str.replace(VALID_CHARACTERS, '')
texts['_text'] = texts['_text'].str.replace(r' {2,}', ' ')


texts['_text'] =texts['_text'].str.replace('\n', ' ') #replace next line with space
texts['_text'] =texts['_text'].str.replace('#', ' ') #separte hashtags
texts['_text'] =texts['_text'].str.replace(',', '') #separte hashtags

texts = texts[~texts['_text'].isna()]


bbm= " ".join(texts[texts['group_candidate']=='Marcos-Duterte']['_text'].values)
leni= " ".join(texts[texts['group_candidate']=='Leni-Kiko']['_text'].values)
isko= " ".join(texts[texts['group_candidate']=='Isko-Ong']['_text'].values)
news = " ".join(texts[texts['group_candidate'].isin(['phil-star','manila-bullletin'])]['_text'].values)

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords=STOP_WORDS_SOURCE,
                min_font_size = 10).generate(leni)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()