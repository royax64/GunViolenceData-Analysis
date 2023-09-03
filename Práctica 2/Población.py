import requests, zipfile, pandas as pd
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

#Descarga y limpia un archivo csv con la población de todos los condados de EUA, datos del año 2020.

fileName = "DECENNIALDHC2020.P1-Data.csv"

def dataDownload(url: str):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path="./", members=[fileName])

def main():
    dataDownload("https://data.census.gov/api/access/table/download?download_id=ca4425f0f7783a5009e1c3b4a62c304fb8fc6df25e36187dadcc0c4b11c4a47b")
   
    #Quitando columnas innecesarias, cambiando nombres de columnas y reorganizando
    #un poco.
    
    df = pd.read_csv(fileName)
    df = df.drop(["GEO_ID","P1_001NA", "Unnamed: 4"], axis=1) 
    df = df.drop(index=df.index[0], axis=0)  
    df = df.rename(columns={'P1_001N':'2020_Population'}) 
    df[['County','State']] = df.NAME.str.split(", ",expand=True)
    df = df.drop("NAME", axis=1)
    df = df[['State','County','2020_Population']]
    df.at[1,'State'] = 'United States'

    #Quitando posibles espacios en blanco.
    df.State = df.State.str.lstrip()
    df.State = df.State.str.rstrip()
    df.County = df.County.str.lstrip()
    df.County = df.County.str.rstrip()
    df['2020_Population'] = df['2020_Population'].str.strip()
    
    df.to_csv(fileName)

if __name__ == "__main__":
    main()
