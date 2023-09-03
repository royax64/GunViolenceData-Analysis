import re, pandas as pd, numpy as np

#La información fué obtenida a partir de web scraping en gunviolencearchive.org

'''TODO:
    -> Población del área
    -> Validar todas las columnas.
    -> Validad los campos vacíos, principalmente dónde no hay un conteo de arma.
'''

def eliminarColumnasInnecesarias(df: pd.DataFrame) -> pd.DataFrame:
    columnasAEliminar = [
            'incident_url', #URL fuente, es la misma información que el csv
            'incident_url_fields_missing',  #Toda la columna es False.
            'congressional_district', #Probablemente irrelevante para el análisis.
            'state_house_district',
            'state_senate_district',
            'Unnamed: 0'
            ]
    return df.drop(columnasAEliminar, axis=1)

quitarEspaciosEnBlanco = {
        'source_url': str.strip,
        'sources': str.strip,
        'date': str.strip,
        'state': str.lstrip,
        'state': str.rstrip,
        'city_or_county': str.lstrip,
        'city_or_county': str.rstrip,
        'address': str.lstrip,
        'address': str.rstrip,
        'n_killed': str.strip,
        'n_injured': str.strip,
        'gun_stolen': str.strip,
        'gun_type': str.lstrip,
        'gun_type': str.rstrip,
        'incident_characteristics': str.lstrip,
        'incident_characteristics': str.rstrip,
        'latitude': str.strip,
        'location_description': str.lstrip,
        'location_description': str.rstrip,
        'longitude': str.strip,
        'n_guns_involved': str.strip,
        'notes': str.lstrip,
        'notes': str.rstrip,
        'participant_age': str.strip,
        'participant_age_group': str.strip,
        'participant_gender': str.strip,
        'participant_name': str.lstrip,
        'participant_name': str.rstrip,
        'participant_relationship': str.lstrip,
        'participant_relationship': str.rstrip,
        'participant_status': str.strip,
        'participant_type': str.strip,
        }

def juntarColumnasURLs(df: pd.DataFrame) -> pd.DataFrame:
    def concatenandoURLs(fila):
        if ((not fila['surl_in_ss'])):
            return f"{fila['sources']}||{fila['source_url']}"
        else:
            return fila['sources']
            
    df['sources'] = df.apply(concatenandoURLs, axis=1)
    df.sources = df.sources.str.lstrip("||")

    return df

def main():
    df = pd.read_csv("../2013-01_2018-03.csv", converters=quitarEspaciosEnBlanco)
    df2 = eliminarColumnasInnecesarias(df)
        
    #Validando urls en la columna source_url, si no, entonces que sean NaN
    url_check = re.compile('((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)')
    df2['valid_url'] = df.source_url.replace(to_replace = url_check, value = 'valid', regex=True)
    df2.loc[df2.valid_url != 'valid', 'source_url'] = np.nan

    #Checando si la URL de source_url existe en sources
    df2['surl_in_ss'] = [((str(x[0]) in str(x[1])) or x[2]) for x in zip(df2.source_url, df2.sources, df2.source_url.isnull())]

    #Si es así, entonces juntando columnas sources y source_url 
    df3 = juntarColumnasURLs(df2)

    
    #Eliminando más columnas innecesarias, reordenando y escribiendo a un csv
    df4 = df3.drop(['source_url','valid_url','surl_in_ss'], axis=1)
    df4 = df4[['date','state','city_or_county','address','latitude','longitude','location_description','incident_characteristics','notes','n_guns_involved','gun_type','gun_stolen','n_injured','n_killed','participant_name','participant_age','participant_age_group','participant_gender','participant_type','participant_relationship','participant_status','sources']]

    df4.to_csv("2013-01_2018-03.csv")

if __name__ == "__main__":
    main()
