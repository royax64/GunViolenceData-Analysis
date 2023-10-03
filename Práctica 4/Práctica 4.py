import pandas as pd
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go
from dateutil import parser
import datetime

#Práctica 4: Data visualization
#Este script genera un archivo HTML interactivo y una imagen en png.

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
    perStatusAndType = pd.read_csv('../Práctica 3/porEstatusYTipo.csv')
    perGenderAndType = pd.read_csv('../Práctica 3/porGeneroYTipo.csv', index_col=0)
    perAgeGroupAndType = pd.read_csv('../Práctica 3/porGrupoEdadyTipo.csv', index_col=0)
    perGunStolen = pd.read_csv('../Práctica 3/porPistolaRobada.csv', index_col=0)
    perParticipantRelationship = pd.read_csv('../Práctica 3/porRelacionDeParticipantes.csv', index_col=0)
    perGunType = pd.read_csv('../Práctica 3/porTipoPistola.csv', index_col=0)
    perAge = pd.read_csv('../Práctica 3/porEdadParticipante.csv')

    #Renombrando dataframes
    perParticipantType.rename(columns = {'participant_age':'total_people'}, inplace = True)
    incidentsPerYear.rename(columns = {'sources':'incidents'}, inplace = True)
    incidentsPerDay.rename(columns = {'sources':'incidents'}, inplace = True)
    incidentsPerMonth.rename(columns = {'sources':'incidents'}, inplace = True)
    incidentsPerState.rename(columns = {'date':'incidents'}, inplace = True)
    perStatusAndType.rename(columns = {'participant_age_group':'total_people'}, inplace = True)
    perGenderAndType.rename(columns = {'pairticipant_age':'total_people'}, inplace = True)
    perAgeGroupAndType.rename(columns = {'participant_age':'total_people'}, inplace = True)
    perGunStolen.rename(columns = {'gun_type':'total_guns'}, inplace = True)
    perParticipantRelationship.drop('participant_type', axis=1, inplace = True)
    perParticipantRelationship.rename(columns = {'participant_age_group':'incidents'}, inplace = True)
    perGunType.rename(columns = {'gun_stolen':'total_guns'}, inplace = True)   

    """ 
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
    print(perAgeperAgeGroupAndType)
    print(perGunStolen)
    print(perParticipantRelationship)
    print(perGunType)
    print(perAge)
    """

    ###Fig 1: Localización de todos los eventos
    GVDdf['IncidentInfo'] = GVDdf.date + '\n' + GVDdf.address + '\n' + GVDdf.notes #Subtitulo de cada punto

    everyIncidentMap = go.Figure(data=go.Scattergeo(
        lon = GVDdf.longitude,
        lat = GVDdf.latitude,
        text = GVDdf['IncidentInfo'],
        mode = 'markers',
        ))

    everyIncidentMap.update_layout(
        title = 'Violencia con armas de fuego en los Estados Unidos desde 2013 hasta 2018',
        geo_scope='usa',
    )

    pt.offline.plot(everyIncidentMap, filename="mapaTodosLosCasos.html")
    everyIncidentMap.write_image("mapaTodosLosCasos.png")

    ##Fig 2: Incidentes al paso del tiempo
    evolIncidentsTime = px.line(incidentsPerDay, x=incidentsPerDay.index, y='incidents', title='Cantidad de incidentes de violencia de armas de fuego en los Estados Unidos desde Enero del 2013 hasta Marzo del 2018')
    pt.offline.plot(evolIncidentsTime, filename="incidentesAlPasoDelTiempo.html")
    evolIncidentsTime.write_image("incidentesAlPasoDelTiempo.png")
   
    ##Fig 3: Genero de las víctimas y de los victimarios
    vicSusGender = px.sunburst(perGenderAndType, path=[perGenderAndType.index,'participant_type'], values='participant_age')
    pt.offline.plot(vicSusGender, filename="generoDeVictimasSuspechosos.html")
    vicSusGender.write_image("generoDeVictimasSuspechosos.png")

    ##Fig 4: Marcas de pistolas y tipos más utilizados
    mostUsedGuns = px.pie(perGunType, values='total_guns', names=perGunType.index, title='Tipos de pistolas más utilizadas para violencia de armas')
    pt.offline.plot(mostUsedGuns, filename="tiposPistolasMasUsadas.html")
    mostUsedGuns.write_image("tiposPistolasMasUsadas.png")

    ##Fig 5: Incidentes por estado (La densidad de población claramente importa)
    #Necesito las coordenadas de los estados
    containsCode4State = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')[['code', 'state']]
    incidentsPerState = incidentsPerState.merge(containsCode4State, left_on='state', right_on='state', how='left')
    amountIncidentsPerState = px.choropleth(incidentsPerState, locationmode='USA-states', locations='code', color='incidents',
                                            color_continuous_scale="Reds",
                                            scope="usa",
                          )
    amountIncidentsPerState.update_layout(title_text = 'Cantidad total de incidentes por estado', margin={"r":0,"t":0,"l":0,"b":0})
    pt.offline.plot(amountIncidentsPerState, filename="incidentesPorEstado.html")
    amountIncidentsPerState.write_image("incidentesPorEstado.png")

    ##Fig 6: Cantidad de incidentes por N número de muertos 
    perDeathCount = GVDdf.groupby(['n_killed']).count()
    deathCountBox = px.bar(perDeathCount, x = perDeathCount.index , y=perDeathCount.date)
    pt.offline.plot(deathCountBox, filename="cantidadDeMuertos.html")
    deathCountBox.write_image("cantidadDeMuertos.png")

    ##Fig 7: Cantidad de incidentes por N número de heridos
    perInjuryCount = GVDdf.groupby(['n_injured']).count()
    injuredCountBox = px.bar(perInjuryCount, x = perInjuryCount.index , y=perInjuryCount.date)
    pt.offline.plot(injuredCountBox, filename="cantidadDeHeridos.html")
    injuredCountBox.write_image("cantidadDeHeridos.png")

    ##Fig 8: Por relación entre participantes
    participantRelationshipPie = px.pie(perParticipantRelationship, values='incidents', names=perParticipantRelationship.index, color_discrete_sequence=px.colors.sequential.RdBu, title='Relaciones entre agresor y victima')
    pt.offline.plot(participantRelationshipPie, filename="relacionesEntreParticipantes.html")
    participantRelationshipPie.write_image("relacionesEntreParticipantes.png")
    
    ##Fig 9: Porcentaje de el paradero de las pistolas (robadas o no)
    #NOTA: En la tabla original hay 3 casos: Robada, no-robada y desconocido. En este pie chart
    #se juntaron los casos de desconocido y no-robada.
    wasGunStolenPie = px.pie(perGunStolen, values='total_guns', names=perGunStolen.index, color_discrete_sequence=px.colors.sequential.Greens, title='Paradero de la pistola')
    pt.offline.plot(wasGunStolenPie, filename="paraderoDePistola.html")
    wasGunStolenPie.write_image("paraderoDePistola.png")
    
    ##Fig 10: Ubicaciones con más incidencias.
    mostViolentLocations  = px.pie(locationsMostUsed, values='Frequency', names='Word', title='Top 14 ubicaciones más violentas', color_discrete_sequence=px.colors.sequential.YlGn)
    pt.offline.plot(mostViolentLocations, filename="ubicacionesMasViolentas.html")
    mostViolentLocations.write_image("ubicacionesMasViolentas.png")

    ##Fig 11: Atributos de los incidentes
    commonincidentAttributes  = px.pie(characteristicsMostUsed, values='Frequency', names='Word', title='Atributos y caracteristicas de todos los incidentes', color_discrete_sequence=px.colors.sequential.Blues)
    pt.offline.plot(commonincidentAttributes, filename="caracteristicasDeLosIncidentes.html")
    commonincidentAttributes.write_image("caracteristicasDeLosIncidentes.png")

    ##Fig 12: Edad de los participantes (victimas y victimarios)
    vicSusAgeGroup = px.sunburst(perAgeGroupAndType, path=['participant_age_group',perAgeGroupAndType.index], values='total_people')
    pt.offline.plot(vicSusAgeGroup, filename="edadDeVictimasSuspechosos.html")
    vicSusAgeGroup.write_image("edadDeVictimasSuspechosos.png")

    ##Fig 13: Estátus de los participantes (victimas y victimarios)
    vicSusStatus = px.sunburst(perStatusAndType, path=['participant_type', perStatusAndType.index], values='total_people')
    pt.offline.plot(vicSusStatus, filename="estatusDeVictimasSuspechosos.html")
    vicSusStatus.write_image("estatusDeVictimasSuspechosos.png")

    ##Fig 14: Cantidad de heridos (Box)
    cantidadHeridosBox = px.box(incidentsPerHThousand, y='n_injured', points='all', title='Cantidad acomulada de heridos en EUA por Estado')
    pt.offline.plot(cantidadHeridosBox, filename="promedioCantidadHeridos.html")
    cantidadHeridosBox.write_image("promedioCantidadHeridos.png")
    
    ##Fig 15: Cantidad de muertos (Box)
    cantidadMuertosBox = px.box(incidentsPerHThousand, y='n_killed', points='all', title='Cantidad acomulada de muertos en EUA por Estado')
    pt.offline.plot(cantidadMuertosBox, filename="promedioCantidadMuertos.html")
    cantidadMuertosBox.write_image("promedioCantidadMuertos.png")
    
    ##Fig 16: Muertos y heridos por cada 100,000 habitantes.
    incidentsPerHThousand = incidentsPerHThousand.merge(containsCode4State, left_on='state', right_on='state', how='left')
    deathsAndInjuriesPerH1000ByState = px.choropleth(incidentsPerHThousand, locationmode='USA-states', locations='code', color='deathsPerHThousand',color_continuous_scale="Purples",scope="usa", hover_data=['injuriesPerHThousand','n_injured','n_killed', '2020_Population'])
    deathsAndInjuriesPerH1000ByState.update_layout(title_text = 'Cantidad de muertos y heridos por cada 100,000 habitantes', margin={"r":0,"t":0,"l":0,"b":0})
    pt.offline.plot(deathsAndInjuriesPerH1000ByState, filename="muertesyHeridosPorCada100000PorEstado.html")
    deathsAndInjuriesPerH1000ByState.write_image("muertesyHeridosPorCada100000PorEstado.png")

    ##Fig 17: Por cantidad de involucrados por edad.
    cantidadParticipantesEdad = px.histogram(perAge, x=perAge.index, y='total_amount_people')
    pt.offline.plot(cantidadParticipantesEdad, filename="cantidadParticipantesPorEdad.html")
    cantidadParticipantesEdad.write_image("cantidadParticipantesPorEdad.png")

    
if __name__ == "__main__":
    main()
