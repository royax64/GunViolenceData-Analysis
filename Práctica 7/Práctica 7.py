import pandas as pd
import plotly as pt
import plotly.express as px
import numpy as np

#Práctica 7: Algoritmo de clasificación de puntos (n vecinos más cercanos)

#Function that makes scatter plots given a dataframe, x, y and z coordinates and a filename to save to.
def doFigure(df: pd.DataFrame, myX: str, myY: str, myZ: str, myFilename: str):
    fig = px.scatter(df, x=myX, y=myY, color=myZ)
    pt.offline.plot(fig, filename=myFilename+'.html')
    fig.write_image(myFilename+'.png')

# doNearestNeighbors(k: int, df: pd.DataFrame, newPoints: np.array) -> pd.DataFrame:
#   args:
#       -> k (int): n nearest points to the new point given.
#       -> df: DataFrame with the data (x, y, z)
#       -> newPoints: Array of points (x, y) 
#
#   Function that calculates the Z coordinate of newPoints given a
#   dataframe of points with known value based on their distances.
#   Returns a new DataFrame with the new points appended to the given set
#   of points

def doNearestNeighbors(k: int, df: pd.DataFrame, newPoints: np.array) -> pd.DataFrame:
    distance = lambda p1, p2:  np.linalg.norm(p1 - p2) #Np arrays as input
    auxDF = df
    for point in newPoints:
        auxDF['listPoints'] = auxDF[['n_participants','n_guns_involved']].values.tolist()
        auxDF['listPoints'] = np.array(auxDF['listPoints'])
        auxDF['distanceToNewPoint'] = auxDF.apply(lambda row: distance(point, row.listPoints), axis=1)
        kNearestPointsDF = auxDF.sort_values('distanceToNewPoint').head(k)
        newZcoordinate = kNearestPointsDF.iloc[:, 3].mean()
        df.loc[len(df)] = ['null', point[0], point[1], newZcoordinate, 'null', 'null']

    return df.iloc[:, 1:4]

def main():
    GVDdf = pd.read_csv('../Práctica 5/2013-01_2018-03.csv')
    
    #Gráfica 1: 
    # X -> n_participants
    # Y -> n_guns_involved
    # Z -> n_injured
    #Notas: Se ignoran los casos sin el dato de número de pistolas.
    peopleGunsInjuredDF = GVDdf[['n_participants','n_guns_involved','n_injured']]
    peopleGunsInjuredDF = peopleGunsInjuredDF.dropna()
    peopleGunsInjuredDF = peopleGunsInjuredDF.reset_index()
    doFigure(
            peopleGunsInjuredDF,
            'n_participants',
            'n_guns_involved',
            'n_injured',
            'antesFigNGentesPistolasHeridos'
            )
    newPoints = np.random.randint(0, 100, size=(20,2))
    pGIwithNewPointsDF = doNearestNeighbors(5, peopleGunsInjuredDF, newPoints)
    print(pGIwithNewPointsDF.tail(30))
    doFigure(
            pGIwithNewPointsDF,
            'n_participants',
            'n_guns_involved',
            'n_injured',
            'prediccionFigNGentesPistolasHeridos'
            )

    #Gráfica 2: 
    # X -> n_participants
    # Y -> n_guns_involved
    # Z -> n_killed
    #Notas: Se ignoran los casos sin el dato de número de pistolas.
    peopleGunsKilledDF = GVDdf[['n_participants','n_guns_involved','n_killed']]
    peopleGunsKilledDF = peopleGunsKilledDF.dropna()
    peopleGunsKilledDF = peopleGunsKilledDF.reset_index()
    doFigure(
            peopleGunsKilledDF,
            'n_participants',
            'n_guns_involved',
            'n_killed',
            'antesFigNGentesPistolasMuertos'
            )
    newPoints = np.random.randint(0, 100, size=(20,2))
    pGKwithNewPointsDF = doNearestNeighbors(5, peopleGunsKilledDF, newPoints)
    print(pGKwithNewPointsDF.tail(30))
    doFigure(
            pGKwithNewPointsDF,
            'n_participants',
            'n_guns_involved',
            'n_killed',
            'prediccionFigNGentesPistolasMuertos'
            )

if __name__ == '__main__':
    main()
