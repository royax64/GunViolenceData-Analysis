import pandas as pd
import plotly.express as px
import plotly as pt
import datetime
from dateutil import parser
#Práctica 6: Regresión Lineal


#Función que toma un string con una fecha y lo convierte a un número sin guiones ni espacios.
#INPUT: '2020-12-23'
#OUTPUT: 20201223

def returnDateInt(row):
        newdate = parser.parse(row) #Convierte a objeto datetime
        return int(newdate.strftime('%Y%m%d'))

#Hace la regresión lineal en plotly e guarda las gráficas. Retorna el resultado para imprimir.
def doLinearRegression(df: pd.DataFrame, myX: str, myY: str, myFilename: str) -> str:
    lr = px.scatter(df, x=myX, y=myY, trendline='ols')
    pt.offline.plot(lr, filename=myFilename+'.html')
    lr.write_image(myFilename+'.png')
    lrModel = px.get_trendline_results(lr).px_fit_results.loc[0]
    lrModelResult = lrModel.summary()
    return lrModelResult

def main():
    GVDdf = pd.read_csv('../Práctica 5/2013-01_2018-03.csv', index_col=0)

    #Regresión Lineal de las personas participantes vs personas muertas
    #x = n_participants -> y = n_killed
    lrNumPeopleANDkilled = doLinearRegression(GVDdf, 'n_participants', 'n_killed', 'RegLinealNumPersonasyMuertos')
    print('Regresión lineal de las personas participants vs muertas\n', lrNumPeopleANDkilled)
    
    #Segunda regresión lineal de las personas participantes vs personas heridas.
    #x = n_participants -> y = n_injured
    lrNumPeopleANDinjured = doLinearRegression(GVDdf, 'n_participants', 'n_injured', 'RegLinealNumPersonasyHeridas')
    print('\nRegresión lineal de las personas participants vs heridas\n', lrNumPeopleANDinjured)

    #Tercera RL: Dia y número de casos casos
    #x = date -> y = numCases
    perDay = pd.read_csv('../Práctica 3/casosPorDia.csv')
    perDay.rename(columns={'sources':'numCases'}, inplace=True)
    perDay['date'] = perDay['date'].apply(returnDateInt)

    lrDayNumCases = doLinearRegression(perDay, 'date', 'numCases', 'RegLinealDiaNumCasos')
    print('\nRegresión lineal del día vs cantidad de casos\n', lrDayNumCases)

    #Cuarta RL: Edad y cantidad de participantes de esa edad.
    #x = 'participant_age' -> y = 'amount_people'
    perAge = pd.read_csv('../Práctica 3/porEdadParticipante.csv')
    perAge.rename(columns={'total_amount_people':'amount_people'}, inplace=True) #Más simplicidad

    lrPerAge = doLinearRegression(perAge, 'participant_age', 'amount_people', 'RegLinealEdadPersonasyCantidad')
    print('\nRegresión lineal de las edades y la cantidad de personas\n', lrPerAge)

if __name__ == "__main__":
    main()

