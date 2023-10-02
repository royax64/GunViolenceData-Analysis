import pandas as pd
import plotly.express as px
import plotly as pt
#Práctica 6: Regresión Lineal

def main():
    GVDdf = pd.read_csv('../Práctica 5/2013-01_2018-03.csv', index_col=0)

    #Regresión Lineal de las personas participantes vs personas muertas
    #x = n_participants -> y = n_killed

    lrNumPeopleANDkilled = px.scatter(GVDdf, x='n_participants', y='n_killed', trendline='ols')
    pt.offline.plot(lrNumPeopleANDkilled, filename="RegLinealNumPersonasyMuertos.html")
    lrNumPeopleANDkilled.write_image("RegLinealNumPersonasyMuertos.png")
    lrNumPeopleANDkilledModel = px.get_trendline_results(lrNumPeopleANDkilled).px_fit_results.loc[0]
    lrNumPeopleANDkilledModelResult = lrNumPeopleANDkilledModel.summary()
    print('Regresión lineal de las personas participants vs muertas\n', lrNumPeopleANDkilledModelResult)
    

    

if __name__ == "__main__":
    main()

