#Práctica 3: Pruebas Estadisticas Descriptivas
#Este script imprime los resultados.
import pandas as pd

def main():
    
    GVDdf = pd.read_csv("../Práctica 2/2013-01_2018-03.csv", index_col=0)
    populationDF = pd.read_csv("../Práctica 2/DECENNIALDHC2020.P1-Data.csv", index_col=0)
    
    #Agrupando por población de estados
    populationStateDF = populationDF.groupby(by='State', sort=False).sum().reset_index()[['State', '2020_Population']]
    GVDState = GVDdf.groupby(by='state')

    #Casos por estado
    casesPerState = GVDState.count().reset_index()
    casesPerState = casesPerState[['state','date']].sort_values('date').reset_index(drop=True)
    print(f"El estado con más incidentes de violencia con armas es {casesPerState.at[50,'state']} con {casesPerState.at[50,'date']} y el que tiene menos es {casesPerState.at[0,'state']} con {casesPerState.at[0,'date']}")
    casesPerState.to_csv('casosPorEstado.csv')

    #Agrupando por estados, esta vez sumando las filas.
    GVDSumState = GVDState[['n_injured','n_killed']].sum()

    #Uniendo las poblaciones a la tabla de casos.
    GVDSumState = GVDSumState.merge(populationStateDF, left_on='state', right_on='State', how='left')
    GVDSumState.rename({'State':'state'},axis=1,inplace=True)
    GVDSumState.set_index('state', inplace=True)

    #Muertos y heridos cada 100,000 habitantes de cada estado
    perHThousand = GVDSumState.assign(deathsPerHThousand = (GVDSumState['n_killed'] / GVDSumState['2020_Population'])*100000, injuriesPerHThousand = (GVDSumState['n_injured'] / GVDSumState['2020_Population'])*100000)
    perHThousand = perHThousand.sort_values('deathsPerHThousand')
    print(f"El estado con más muertes por cada 100,000 habitantes es: \n{perHThousand.tail(1)[['deathsPerHThousand']]}\n\ny el que tiene menos es: \n{perHThousand.head(1)[['deathsPerHThousand']]}")
    perHThousand.to_csv('MuertesPorCadaCienMil.csv')   


if __name__ == "__main__":
    main()
