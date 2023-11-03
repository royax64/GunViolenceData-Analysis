import pandas as pd
import plotly as pt
import plotly.express as px
import numpy as np
import datetime as dt
from typing import Tuple

#Práctica 8: Algoritmo de agrupamiento de puntos (k means)

#Function that makes scatter plots given a dataframe, the centroids, x, y and z coordinates and a filename to save to.
def doFigure(df: pd.DataFrame, centroids: np.array, myX: str, myY: str, myZ: str, myFilename: str):
    df['plt_size'] = 1
    for i, c in enumerate(centroids): #Adding centroids to df to plot with different size
        df.loc[len(df.index)] = [c[0], c[1], i, 3]
    fig = px.scatter(df, x=myX, y=myY, color=myZ, size='plt_size')
    pt.offline.plot(fig, filename=myFilename+'.html')
    fig.write_image(myFilename+'.png')

# doKMeans(k: int, df: pd.DataFrame, x: str, y: str, iterations: int) -> Tuple[pd.DataFrame, np.array]:
#   args:
#       -> k (int): make k groups to group data by.
#       -> df: DataFrame with the data (x, y).
#       -> x: x-axis of points
#       -> y: y-axis of points
#       -> iterations: #times to iterate the new centroids
#   
#   returns:
#        -> df with closest centroid for each point
#       INPUT:                          OUTPUT:
#           num_injured Num_killed          num_injured num_killed centroid
#       0       4           5           0         4           5       1
#       1       2           5           1         2           5       2  
#       2       4           9           2         4           9       1
#
#        -> numpy array with optimized centroids
#
#       Categorizes the dataframe into k distinct groups, each group is made according to the nearest points
#       from a centroid, then repeatedly calculating new centroids based on the average of the points in that group.

def doKMeans(k: int, df: pd.DataFrame, x: str, y: str, iterations: int) -> Tuple[pd.DataFrame, np.array]:
    newCentroidX = np.random.randint(df[x].min(), df[x].max(), size=k)
    newCentroidY = np.random.randint(df[y].min(), df[y].max(), size=k)
    newCentroids = np.stack((newCentroidX, newCentroidY), axis=1)
    
    def findClosestCentroid(row) -> str:
        row = row[[x,y]].to_numpy().astype(np.float64)
        distances = np.linalg.norm(row - newCentroids, axis=1)
        return str(np.argmin(distances))
    
    for i in range(iterations):
        df['nearestCentroid'] = df.apply(findClosestCentroid, axis=1)
        
        for i, centroid in enumerate(newCentroids):
            group = df[df['nearestCentroid'] == str(i)]
            if not group.empty:
                newCentroids[i] = np.array(group[[x,y]].mean())

    return (df, newCentroids)

def main():
    GVDdf = pd.read_csv('../Práctica 5/2013-01_2018-03.csv', index_col=0)

    #Gráfica 1: 
    # X -> n_participants
    # Y -> n_injured
    #Notas: Se ignoran los casos sin el dato de número de pistolas.
    numPplInjuredDF = GVDdf[['n_participants','n_injured']]
    numPplInjuredDF = numPplInjuredDF.dropna()
    numPplInjuredClassifiedDF, centroids = doKMeans(3, numPplInjuredDF, 'n_participants', 'n_injured', 3) 
    doFigure(
            numPplInjuredClassifiedDF,
            centroids,
            'n_participants',
            'n_injured',
            'nearestCentroid',
            'cantidadPistolasHeridosClasificado'
            )

    #Gráfica 2: 
    # X -> n_guns_involved
    # Y -> n_killed
    #Notas: Se ignoran los casos sin el dato de número de pistolas.
    gunsPplKilledDF = GVDdf[['n_guns_involved','n_killed']]
    gunsPplKilledDF = gunsPplKilledDF.dropna()
    gunsPplKilledClassifiedDF, centroids = doKMeans(3, gunsPplKilledDF, 'n_guns_involved', 'n_killed', 4)
    doFigure(
            gunsPplKilledClassifiedDF,
            centroids,
            'n_guns_involved',
            'n_killed',
            'nearestCentroid',
            'cantidadPistolasMuertosClasificado'
            )
    
    #Familia de gráficas:
    # X -> date (2013..2018)
    # Y -> num_casos
    perDay = pd.read_csv('../Práctica 3/casosPorDia.csv')
    perDay.rename(columns={'sources':'numCases'}, inplace=True)
    perDay['date'] = pd.to_datetime(perDay['date'])
    for year in perDay['date'].dt.year.unique():
        yearDF = perDay[perDay['date'].dt.year == year].copy()
        yearDF['date'] = yearDF['date'].apply(lambda row: int(row.strftime('%Y%m%d')))
        perDayClassifiedDF, centroids = doKMeans(6, yearDF, 'date', 'numCases', 5)
        doFigure(
            perDayClassifiedDF,
            centroids,
            'date',
            'numCases',
            'nearestCentroid',
            f'temporadasDelAño{year}'
            )

if __name__ == '__main__':
    main()
