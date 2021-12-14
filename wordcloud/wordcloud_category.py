# !pip install wordcloud
# !pip install matplotlib
# !pip install krwordrank

import pandas as pd
import numpy as np

from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import requests

import matplotlib.pyplot as plt 
import argparse

def displayWordCloud(data,
                     pont_path,
                     mask_image, 
                     stopwords_kr):
    
    """
    Explanation
         The Worldcloud's shape is set according to the top.
         If you want me to dress you up, bring a picture.

    Args:
        data: Tokenized noun word list
        custom_mask: Wordcloud shape you want
        stopwords_kr: Words that are not included in the wordcloud
    
    Print:    
        Print the word cloud picture and the relative numbersI(importance) of each word.
    """
        
    wordcloud = WordCloud(
        font_path=pont_path,        
        stopwords= stopwords_kr, 
        background_color = 'white', 
        max_words=40,
        contour_color='brown',
        mask = mask_image).generate(data)
    
    
    plt.figure(figsize = (20,20))
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis("off") 
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', type=str, default='susan', help='about product category')
    args = parser.parse_args()

    stopwords_kr =['건','개','점','건','특','중','햇','수','과','대','미','호','특대', 'gx봉', 'x박스','x팩', 'x봉','g내외',
               '여수멸치어가','등급','등급이상','cm','이상','법성포','반건조','손질','과내외','gx', '제주','혼합','명품',
               '영광법성포', '프리미엄','내외','명가','이상미','금일','해저식품', '광천','모음전','당도선별 성주','구이죽용',
               '산지직송','국산','굿피쉬','임금님 밥상','대원건어물백화점','세트', '선물세트','영동','구운','국내가공','임금님']
    
    custom_mask = np.array(Image.open("../data/market.png"))
    
    if args.category == 'susan' :
        susan=pd.read_excel('../data/수산물.xlsx')
        susan['수산물'] = susan['수산물'].astype(str) # change type to string
        displayWordCloud(''.join(susan['수산물']), 
                         pont_path = '../data/현대하모니+M.ttf', 
                         mask_image = custom_mask, 
                         stopwords_kr = stopwords_kr)

    elif args.category == 'chuksan' :
        chuksan=pd.read_excel('../data/축산물.xlsx')
        chuksan['축산물'] = chuksan['축산물'].astype(str) # change type to string
        displayWordCloud(''.join(chuksan['축산물']), 
                         pont_path = '../data/현대하모니+M.ttf', 
                         mask_image = custom_mask, 
                         stopwords_kr = stopwords_kr)

    elif args.category == 'nongsan' :
        nongsan=pd.read_excel('../data/농산물.xlsx')
        nongsan['농산물'] = nongsan['농산물'].astype(str) # change type to string
        displayWordCloud(''.join(nongsan['농산물']), 
                         pont_path = '../data/현대하모니+M.ttf', 
                         mask_image = custom_mask, 
                         stopwords_kr = stopwords_kr)
