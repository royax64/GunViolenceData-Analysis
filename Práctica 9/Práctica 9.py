import pandas as pd
import plotly.express as px
import plotly as pt
import datetime as dt
import plotly.graph_objects as go
import numpy as np
from dateutil import parser
#Práctica 9: Regresión Lineal + Varianza (Forecasting)

#Hace la regresión lineal en plotly e guarda las gráficas. Retorna el resultado para imprimir.
def doLRVariance(df: pd.DataFrame, myX: str, myY: str, myFilename: str) -> str:
    lr = px.scatter(df, x=myX, y=myY, trendline='ols')
    lrModel = px.get_trendline_results(lr).px_fit_results.loc[0]
    bounds = np.sqrt(lrModel.mse_resid)
    slope = lrModel.params[1]
    yIntersect = lrModel.params[0]
    xAxis = np.array([float(i) for i in range(int(df[myX].min().round()), int(df[myX].max().round())+ 1)])
    upperY = (xAxis * slope + yIntersect) + bounds
    lowerY = (xAxis * slope + yIntersect) - bounds

    lr.add_trace(go.Scatter(
        x=xAxis.tolist() + xAxis.tolist()[::-1],
        y=upperY.tolist() + lowerY.tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name=f"Error de predicción de {myY}"
        ))

    pt.offline.plot(lr, filename=myFilename+'.html')
    lr.write_image(myFilename+'.png')
    return lrModel.summary()

def main():
    GVDdf = pd.read_csv('../Práctica 5/2013-01_2018-03.csv', index_col=0)

    #Regresión Lineal de las personas participantes vs personas muertas
    #x = n_participants -> y = n_killed
    lrNumPeopleANDkilled = doLRVariance(GVDdf, 'n_participants', 'n_killed', 'RegLinealNumPersonasyMuertos')
    print('Regresión lineal de las personas participants vs muertas\n', lrNumPeopleANDkilled)
    
    #Segunda regresión lineal de las personas participantes vs personas heridas.
    #x = n_participants -> y = n_injured
    lrNumPeopleANDinjured = doLRVariance(GVDdf, 'n_participants', 'n_injured', 'RegLinealNumPersonasyHeridas')
    print('\nRegresión lineal de las personas participants vs heridas\n', lrNumPeopleANDinjured)

    #Familia de Regresiones Lineales: Dia y número de casos casos
    #x = date -> y = numCases
    perDay = pd.read_csv('../Práctica 3/casosPorDia.csv')
    perDay.rename(columns={'sources':'numCases'}, inplace=True)
    perDay['date'] = pd.to_datetime(perDay['date'])
    for year in perDay['date'].dt.year.unique():
        yearDF = perDay[perDay['date'].dt.year == year].copy()
        yearDF['date'] = yearDF['date'].apply(lambda row: int(row.strftime('%Y%m%d')))
        lrDayNumCases = doLRVariance(yearDF, 'date', 'numCases', f"RegLinealDiaNumCasos{year}")
        print(f"\nRegresión lineal diaria del {year} vs cantidad de casos\n", lrDayNumCases)

if __name__ == "__main__":
    main()

