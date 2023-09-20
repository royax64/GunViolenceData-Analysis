#Práctica 3: Pruebas Estadisticas Descriptivas
#Este script imprime los resultados.
import pandas as pd
from collections import Counter


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
    print(f"\nEl estado con más muertes por cada 100,000 habitantes es: \n{perHThousand.tail(1)[['deathsPerHThousand']]}\n\ny el que tiene menos es: \n{perHThousand.head(1)[['deathsPerHThousand']]}\n")
    perHThousand.to_csv('MuertesPorCadaCienMil.csv') 
    #perHThousand.mean(axis=0)

    #Lugar más común (analizando location_description)
    GVDdf['location_description'] = GVDdf['location_description'].fillna('Unknown').str.lower()
    wordsMostUsed = Counter(" ".join(GVDdf['location_description']).split()).most_common(20)
    wordsMostUsedDF = pd.DataFrame(wordsMostUsed, columns=['Word', 'Frequency'])
    print(f"Los lugares con más incidentes son: {', '.join(i for i in wordsMostUsedDF['Word'])}.")
    wordsMostUsedDF.to_csv('localizacionesMasRepetidas.csv')

    #Día, mes y año más violentos (con más incidentes)
    GVDdf.date = pd.to_datetime(GVDdf.date)
    GVDdf.set_index('date',inplace=True)
    perMonth = GVDdf.groupby(pd.Grouper(freq="M")).count()[['sources']]
    perYear = GVDdf.groupby(pd.Grouper(freq="Y")).count()[['sources']]
    perDay = GVDdf.groupby(GVDdf.index).count()[['sources']]
    
    yearMaxCasosFecha = perYear.sources.idxmax().date()
    yearMaxCasos = perYear.loc[str(yearMaxCasosFecha)].sources
    yearMinCasosFecha = perYear.sources.idxmin().date()
    yearMinCasos = perYear.loc[str(yearMinCasosFecha)].sources
    yearMeanCasos = str(perYear.sources.mean())

    mesMaxCasosFecha = perMonth.sources.idxmax().date()
    mesMaxCasos = perMonth.loc[str(mesMaxCasosFecha)].sources
    mesMinCasosFecha = perMonth.sources.idxmin().date()
    mesMinCasos = perMonth.loc[str(mesMinCasosFecha)].sources
    mesMeanCasos = str(perMonth.sources.mean())

    dayMaxCasosFecha = perDay.sources.idxmax().date()
    dayMaxCasos = perDay.loc[str(dayMaxCasosFecha)].sources
    dayMinCasosFecha = perDay.sources.idxmin().date()
    dayMinCasos = perDay.loc[str(dayMinCasosFecha)].sources
    dayMeanCasos = str(perDay.sources.mean())

    print(f"""\nEl año con más incidentes fué {yearMaxCasosFecha.year} con {yearMaxCasos} incidentes, el menor fué {yearMinCasosFecha.year} con {yearMinCasos} incidentes, en promedio {yearMeanCasos} casos al año.
          \nEl mes con más incidentes fué {mesMaxCasosFecha.strftime('%Y-%m')} con {mesMaxCasos} incidentes, el menor fué {mesMinCasosFecha.strftime('%Y-%m')} con {mesMinCasos} incidentes, en promedio {mesMeanCasos} casos al mes.
          \nY el día con más incidentes fué {dayMaxCasosFecha} con {dayMaxCasos} incidentes, el menor fué {dayMinCasosFecha} con {dayMinCasos} incidentes, en promedio {dayMeanCasos} casos al día.""")

    perYear.to_csv('casosPorAño.csv')
    perMonth.to_csv('casosPorMes.csv')
    perDay.to_csv('casosPorDia.csv')

if __name__ == "__main__":
    main()
