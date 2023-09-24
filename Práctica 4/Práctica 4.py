import pandas as pd
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go

def main():
    GVDdf = pd.read_csv("../Práctica 2/2013-01_2018-03.csv", index_col=0)
    perParticipantType = pd.read_csv('../Práctica 3/cantidadTipoParticipante.csv', index_col=0)
    characteristicsMostUsed = pd.read_csv('../Práctica 3/caracteristicasMasRepetidas.csv', index_col=0)
    incidentsPerYear = pd.read_csv('../Práctica 3/casosPorAño.csv', index_col=0)
    incidentsPerDay = pd.read_csv('../Práctica 3/casosPorDia.csv', index_col=0)
    incidentsPerState = pd.read_csv('../Práctica 3/casosPorEstado.csv', index_col=0)
    incidentsPerMonth = pd.read_csv('../Práctica 3/casosPorMes.csv', index_col=0)
    locationsMostUsed = pd.read_csv('../Práctica 3/localizacionesMasRepetidas.csv', index_col=0)
    incidentsPerHThousand = pd.read_csv('../Práctica 3/MuertesPorCadaCienMil.csv', index_col=0)
    perStatusAndType = pd.read_csv('../Práctica 3/porEstatusYTipo.csv', index_col=0)
    perGenderAndType = pd.read_csv('../Práctica 3/porGeneroYTipo.csv', index_col=0)
    perAgeGroupAndType = pd.read_csv('../Práctica 3/porGrupoEdadyTipo.csv', index_col=0)
    perGunStolen = pd.read_csv('../Práctica 3/porPistolaRobada.csv', index_col=0)
    perParticipantRelationship = pd.read_csv('../Práctica 3/porRelacionDeParticipantes.csv', index_col=0)
    perGunType = pd.read_csv('../Práctica 3/porTipoPistola.csv', index_col=0)

    #Renombrando dataframes
    perParticipantType.rename(columns = {'participant_age':'total_people'}, inplace = True)
    incidentsPerYear.rename(columns = {'sources':'incidents'}, inplace = True)
    incidentsPerDay.rename(columns = {'sources':'incidents'}, inplace = True)
    incidentsPerMonth.rename(columns = {'sources':'incidents'}, inplace = True)
    incidentsPerState.rename(columns = {'date':'incidents'}, inplace = True)
    perStatusAndType.rename(columns = {'participant_age_group':'total_people'}, inplace = True)
    perGenderAndType.rename(columns = {'participant_age':'total_people'}, inplace = True)
    perAgeGroupAndType.rename(columns = {'participant_age':'total_people'}, inplace = True)
    perGunStolen.rename(columns = {'gun_type':'total_guns'}, inplace = True)
    perParticipantRelationship.drop('participant_type', axis=1, inplace = True)
    perParticipantRelationship.rename(columns = {'participant_age_group':'incidents'}, inplace = True)
    perGunType.rename(columns = {'gun_stolen':'total_guns'}, inplace = True)   

    '''
    print(perParticipantType)
    print(characteristicsMostUsed)
    print(incidentsPerYear)
    print(incidentsPerDay)
    print(incidentsPerMonth)
    print(locationsMostUsed)
    print(incidentsPerState)
    print(incidentsPerHThousand)
    print(perStatusAndType)
    print(perGenderAndType)
    print(perAgeGroupAndType)
    print(perGunStolen)
    print(perParticipantRelationship)
    print(perGunType)
    '''

    ###Fig 1: Localización de todos los eventos
    GVDdf['IncidentInfo'] = GVDdf.date + '\n' + GVDdf.address + '\n' + GVDdf.notes #Subtitulo de cada punto

    everyIncidentMap = go.Figure(data=go.Scattergeo(
        lon = GVDdf.longitude,
        lat = GVDdf.latitude,
        text = GVDdf['IncidentInfo'],
        mode = 'markers',
        ))

    everyIncidentMap.update_layout(
        title = 'Gun Violence Incidents from 2013 to 2018 (Hover for incident info)',
        geo_scope='usa',
    )

    pt.offline.plot(everyIncidentMap, filename="mapaTodosLosCasos.html")
    everyIncidentMap.write_image("mapaTodosLosCasos.png")

    ##Fig 2: Incidentes al paso del tiempo
    evolIncidentsTime = px.line(incidentsPerDay, x=incidentsPerDay.index, y='incidents', title='Cantidad de incidentes de violencia de armas de fuego en los Estados Unidos desde Enero del 2013 hasta Marzo del 2018')
    pt.offline.plot(evolIncidentsTime, filename="incidentesAlPasoDelTiempo.html")
    evolIncidentsTime.write_image("incidentesAlPasoDelTiempo.png")
    
    ##Fig 3: 
if __name__ == "__main__":
    main()
