import pandas as pd
import statsmodels.api as sm
import json
from statsmodels.formula.api import ols

#Volviendo a aplicar esta función de nuevo, solamente busco obtener el número de participantes por cada caso.
#Favor de ejecutar antes de Práctica 5.py
def getListOfDictFromCustomFormat(column: pd.core.series.Series) -> pd.core.series.Series:
    '''INPUT                        OUTPUT
    Series: Nombre                  Series: Nombre
    0::Royax64||1:Pepito García     [{'0': 'Royax64'},{'1':'Pepito García'}]
    ...                             ...
    ADVERTENCIA: El csv está lleno de edge cases, el código puede parecer espaguetti.
    '''
    
    if column.name == 'index' or column.name == 'date':
        return column

    listColumn = column.str.split('\|') #Algunos rows son partidos por un sólo "|", pero dejará las listas como ['0:Royax64', '', '1:Pepito'] 
 
    def elementoListaADict (row):
        isRowNaN = pd.isna(row)

        try:    #Para diferenciar entre [] y NaN
            isRowNaN = isRowNaN.all()
        except:
            pass

        if isRowNaN: #Si el campo está vacio no procesamos
            return [{'Unknown': 'Unknown'}]

        newRow = []

        for elemento in row: #elemento is a string -> '0::Royax64'

            if elemento == '' or elemento == 'nan':
                continue

            try: #La llave y el elemento son algunas veces separadas por :: o por:
                key, item = elemento.split("::")
            except:
                key, item = elemento.split(":")

            elemento =  json.loads(f"{{\"{key}\":\"{item}\"}}")
            newRow.append(elemento)

        if newRow == []:
            return [{'Unknown': 'Unknown'}]
        else:
            return newRow

    return listColumn.apply(elementoListaADict)

def getNumParticipants(row: pd.core.series.Series) -> int:
    '''INPUT
    Indice   Nombre                                       Status 
    1        [{'0':'Royax64'},{'1':'Pepito García'}]      [{'0':'Dead'}]

    OUTPUT
    2'''
  
    try:
        newcols = row.drop(['index','date']).index
    except:
        newcols = row.drop(['index']).index

    #Cantidad de participantes
    rowQuan = 0
    for propiedad in row[newcols]:
        propiedad = list(propiedad)
        for dicc in propiedad:
            dicc = dict(dicc)
            for key, item in dicc.items():
                if key == 'Unknown':
                    continue
                if int(key) > rowQuan:
                    rowQuan = int(key)
    rowQuan = rowQuan + 1 
    return rowQuan

def main():
    GVDdf = pd.read_csv('../Práctica 2/2013-01_2018-03.csv', index_col=0)

    participantsDF = GVDdf[['participant_age','participant_age_group','participant_gender','participant_type','participant_relationship', 'participant_status']].apply(getListOfDictFromCustomFormat, axis=0).reset_index()
    
    participantsDF['n_participants'] = participantsDF.apply(getNumParticipants, axis=1)

    GVDdf['n_participants'] = participantsDF['n_participants']

    GVDdf.to_csv('2013-01_2018-03.csv')

if __name__ == "__main__":
    main()

