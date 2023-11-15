import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from typing import List

#Práctica 10: Word Cloud
#Makes a word cloud out of location_description and notes

def getWordsFromSeries(series: pd.Series) -> str:
    series = series.dropna()
    text = " ".join(series)
    return text

def doWordCloud(words: str, myFilename: str):
    exclude = ['S','La','El','New','D','hi','y',
               'o','J','of','and','A','or','ar']

    wc = WordCloud(
            width=1000, 
            height=1000,
            background_color='#fdb2c5',
            colormap='magma',
            stopwords=exclude
        ).generate(words)

    plt.figure(figsize=(40,40), facecolor=None)
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(myFilename)
    plt.close()

def main():
    GVDdf = pd.read_csv('../Práctica 5/2013-01_2018-03.csv', index_col=0)

    #Word Cloud 1: Location Description.
    locationDesc = GVDdf['location_description']
    wordsLocationDesc = getWordsFromSeries(locationDesc)
    doWordCloud(wordsLocationDesc, myFilename='NubeDescripcionLugar.png')

    #Word Cloud 2: Incident Notes.
    notes = GVDdf['notes']
    wordsNotes = getWordsFromSeries(notes)
    doWordCloud(wordsNotes, myFilename='NubeNotasDeIncidentes.png')


if __name__ == '__main__':
    main()
