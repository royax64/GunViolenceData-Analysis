#Práctica 3: Pruebas Estadisticas Descriptivas
#Este script imprime los resultados.
import pandas as pd
import json
import numpy as np
from collections import Counter

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

def explodeInfoParticipants(row: pd.core.series.Series) -> pd.DataFrame:
    '''INPUT
    Indice   Nombre                                       Status 
    1        [{'0':'Royax64'},{'1':'Pepito García'}]      [{'0':'Dead'}]

    OUTPUT
    Indice  Nombre              Status
    1       'Royax64'           'Dead'
    1       'Pepito García'     'Unknown' '''
   
    #Columnas a usar, de la misma manera hay muchos edge cases.
    try:
        newcols = row.drop(['index','date']).index
    except:
        newcols = row.drop(['index']).index

    #Cantidad de rows en la forma expandida
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
    rowQuan = rowQuan + 1 #Cantidad de participantes y no el índice mayor

    #Obteniendo los datos y creando la nueva df
    #{'Nombre': ['Royax64', 'Pepito García'], 'Status': ['Dead', 'Unknown']}
    newExpandedData = {}

    for indice, propiedad in enumerate(row[newcols]):
        newParticipantPropData = ['Unknown'] * rowQuan
        for oldData in propiedad:
            for key, value in dict(oldData).items():
                if key == 'Unknown':
                    continue
                newParticipantPropData[int(key)] = value
        newExpandedData[row[newcols].index[indice]] = newParticipantPropData
    
    expandDF = pd.DataFrame(newExpandedData)
    
    #Numero de indice a usar
    expandDF.index = [row['index']] * len(expandDF.index)
    expandDF.rename(columns={'index':'participant_index'})

    return expandDF

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

    print(f"\nEl año con más incidentes fué {yearMaxCasosFecha.year} con {yearMaxCasos} incidentes, el menor fué {yearMinCasosFecha.year} con {yearMinCasos} incidentes, en promedio {yearMeanCasos} casos al año.")
    print(f"El mes con más incidentes fué {mesMaxCasosFecha.strftime('%Y-%m')} con {mesMaxCasos} incidentes, el menor fué {mesMinCasosFecha.strftime('%Y-%m')} con {mesMinCasos} incidentes, en promedio {mesMeanCasos} casos al mes.")
    print(f"Y el día con más incidentes fué {dayMaxCasosFecha} con {dayMaxCasos} incidentes, el menor fué {dayMinCasosFecha} con {dayMinCasos} incidentes, en promedio {dayMeanCasos} casos al día.")

    perYear.to_csv('casosPorAño.csv')
    perMonth.to_csv('casosPorMes.csv')
    perDay.to_csv('casosPorDia.csv')
    
    #Cantidad promedio de pistolas utilizadas
    meanNumberGuns = GVDdf['n_guns_involved'].mean()
    print(f"\nEl promedio de pistolas usadas por incidente es {'%.3f'%(meanNumberGuns)}.")
    
    #Obteniendo las propiedades de los participantes y de las pistolas (genero, edad, etc.)
    print("\nObteniendo información sobre los participantes y pistolas en cada caso...\nEsto tomará unos 15 minutos...")

    participantsGVD = GVDdf[['participant_age','participant_age_group','participant_gender','participant_type','participant_relationship', 'participant_status']].reset_index()
    participantsGVD = participantsGVD.apply(getListOfDictFromCustomFormat, axis=0).reset_index()
    participantsGVD = pd.concat([explodeInfoParticipants(row) for index, row in participantsGVD.iterrows()])

    gunsGVD = GVDdf[['gun_type','gun_stolen']].reset_index()
    gunsGVD = gunsGVD.apply(getListOfDictFromCustomFormat, axis=0).reset_index()
    gunsGVD = pd.concat([explodeInfoParticipants(row) for index, row in gunsGVD.iterrows()])
   
    #Por tipo (víctima o perpetuador)
    totalParticipants = len(participantsGVD.index)
    totalSuspects = participantsGVD.groupby('participant_type').count()[['participant_age']].at['Subject-Suspect', 'participant_age']
    totalVictims = totalParticipants - totalSuspects
    print(f"\nDe todos las {totalParticipants} personas involucradas, {totalSuspects} son suspechosos/perpetuadores y {totalVictims} son víctimas, esto significa que hay una tasa de {totalVictims/totalSuspects} victimas por perpetuador")
    participantsGVD.groupby('participant_type').count()[['participant_age']].to_csv('cantidadTipoParticipante.csv')

    #Por edad y/o grupo de edad.
    participantsGVD.participant_age = participantsGVD.participant_age.replace(to_replace='Unknown', value=np.nan)
    participantsGVD.participant_age = participantsGVD.participant_age.astype('float')
    ageAvr = participantsGVD.participant_age.mean(skipna=True)
    perAgeGroupAndType = participantsGVD.groupby(['participant_type','participant_age_group']).count()[['participant_age']]
    totalAdltSus = 0
    totalAdltVic = 0
    totalTeenSus = 0
    totalTeenVic = 0
    totalChldSus = 0
    totalChldVic = 0

    try:
        totalAdltSus = perAgeGroupAndType.at[('Subject-Suspect', 'Adult 18+'), 'participant_age']
        totalAdltVic = perAgeGroupAndType.at[('Victim', 'Adult 18+'), 'participant_age']
        totalTeenSus = perAgeGroupAndType.at[('Subject-Suspect', 'Teen 12-17'), 'participant_age']
        totalTeenVic = perAgeGroupAndType.at[('Victim', 'Teen 12-17'), 'participant_age']
        totalChldSus = perAgeGroupAndType.at[('Subject-Suspect', 'Child 0-11'), 'participant_age']
        totalChldVic = perAgeGroupAndType.at[('Victim', 'Child 0-11'), 'participant_age']
    except:
        pass

    print(f"\nLa edad promedio de los participantes es de {'%.3f'%(ageAvr)} años.")
    print(f"De todos los perpetuadores {'%.3f'%(100*totalAdltSus/totalSuspects)}% son adultos (18+), {'%.3f'%(100*totalTeenSus/totalSuspects)}% son adolescentes (12-17),  {'%.3f'%(100*totalChldSus/totalSuspects)}% son niños (0-11) y el porcentaje restante tiene edad desconocida.")
    print(f"De todas las victimas {'%.3f'%(100*totalAdltVic/totalVictims)}% son adultos (18+), {'%.3f'%(100*totalTeenVic/totalVictims)}% son adolescentes (12-17), {'%.3f'%(100*totalChldVic/totalVictims)}% son niños (0-11) y el porcentaje restante tiene edad desconocida.")
    perAgeGroupAndType.to_csv('porGrupoEdadyTipo.csv')

    #Por sexo y tipo
    perGenderAndType = participantsGVD.groupby(['participant_gender', 'participant_type'], sort=True).count()[['participant_age']]
    
    totalFemales = perGenderAndType.loc[['Female']].sum().values[0]
    totalMales = perGenderAndType.loc[['Male']].sum().values[0]
    totalFemSus = perGenderAndType.at[('Female', 'Subject-Suspect'), 'participant_age']
    totalFemVic = perGenderAndType.at[('Female', 'Victim'), 'participant_age']
    totalMenSus = perGenderAndType.at[('Male', 'Subject-Suspect'), 'participant_age']
    totalMenVic = perGenderAndType.at[('Male', 'Victim'), 'participant_age']

    print(f"\nDe {totalFemales} mujeres participantes, {totalFemVic} fueron víctimas y {totalFemSus} fueron perpetuadoras ({'%.3f'%(totalFemSus*100/totalFemales)}% de las mujeres participantes son perpetuadoras).")
    print(f"De {totalMales} hombres participantes, {totalMenVic} fueron víctimas y {totalMenSus} fueron perpetuadores ({'%.3f'%(totalMenSus*100/totalMales)}% de los hombres participantes son perpetuadores).")
    perGenderAndType.to_csv('porGeneroYTipo.csv')

    #Porcentaje de suspechosos arrestados y muertos.
    def returnQuery(index: list) -> str:    #Función que une todos los indices que vamos a consultar
        q = ' & (participant_status == \''
        for i in index:
            q = q +  i + '\' | participant_status == \''
        q = q[:-26] + ')' #Elimina el cachito restante y cierra el parentesis
        return q

    perStatusAndType = participantsGVD.groupby(['participant_status', 'participant_type']).count()[['participant_age_group']]
    indexArrested = [i for i in perStatusAndType.index.get_level_values(0) if 'Arrested' in i if 'Killed' not in i]
    indexKilled = [i for i in perStatusAndType.index.get_level_values(0) if 'Killed' in i]
    indexKilled.remove('Killed') #ELIMINAR REPETIDOS 
    numSusArrested = perStatusAndType.query('participant_type == \'Subject-Suspect\'' + returnQuery(indexArrested)).sum().values[0]
    numSusKilled = perStatusAndType.query('participant_type == \'Subject-Suspect\'' + returnQuery(indexKilled)).sum().values[0]
    numVicArrested = perStatusAndType.query('participant_type == \'Victim\'' + returnQuery(indexArrested)).sum().values[0]
    print(f"\nEl porcentaje de victimarios arrestadas es del {'%.3f'%(numSusArrested*100/totalSuspects)}%, del resto el {'%.3f'%(numSusKilled*100/totalSuspects)}% fueron matados y el resto quedó inpune")
    print(f"El porcentaje de víctimas arrestados es del {'%.3f'%(numVicArrested*100/totalVictims)}%.")
    perStatusAndType.to_csv('porEstatusYTipo.csv')

    #Relación más común entre las victimas y sus victimarios
    perParticipantRelationship = participantsGVD.groupby(['participant_relationship', 'participant_type']).count()
    perParticipantRelationship = perParticipantRelationship.query('participant_type == \'Subject-Suspect\'')[['participant_age_group']].sort_values(by=['participant_age_group'], ascending=False)
    perParticipantRelationship.reset_index(level='participant_type', inplace=True)
    print(f"\nLas relaciones más comunes entre la victima y los victimarios son:\n{perParticipantRelationship[['participant_age_group']]}\n")
    perParticipantRelationship.to_csv('porRelacionDeParticipantes.csv')

    #Examina incident_characteristics (razones más comúnes, por género y edad)
    GVDdf.incident_characteristics = GVDdf.incident_characteristics.fillna('Unknown').str.lower()
    characteristicsMostUsed = Counter(" ".join(GVDdf['incident_characteristics']).split('||')).most_common(20)
    characteristicsMostUsedDF = pd.DataFrame(characteristicsMostUsed, columns=['Word', 'Frequency'])
    print(f"\nLos caracteristicas de los incidentes más comunes son: {', '.join(i for i in characteristicsMostUsedDF['Word'])}.")
    characteristicsMostUsedDF.to_csv('caracteristicasMasRepetidas.csv')

    #How many guns stolen
    totalGuns = len(gunsGVD.index)
    gunsGVD.gun_stolen = gunsGVD.gun_stolen.replace(to_replace='Unknown', value='Stolen')
    perGunStolen = gunsGVD.groupby('gun_stolen').count()
    gunStolen = perGunStolen.loc['Stolen'].values[0]
    gunNotStolen = totalGuns - gunStolen
    print(f"\nSolamente el {'%.3f'%(gunNotStolen*100/totalGuns)}% de las pistolas no fueron robadas, el resto se desconoce su paradero o fue robada.")
    perGunStolen.to_csv('porPistolaRobada.csv')

    #Most Used Gun
    perGunType = gunsGVD.groupby('gun_type').count().sort_values(by=['gun_stolen'], ascending=False)
    perGunType.drop(['Unknown'], inplace=True)
    print(f"La pistola más usada es {perGunType.index[0]}")
    perGunType.to_csv('porTipoPistola.csv')


if __name__ == "__main__":
    main()
