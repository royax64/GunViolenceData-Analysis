import requests, tarfile, pandas as pd

#El link te da un archivo .tar.gz a extraer.

fileName = '2013-01_2018-03.tar.gz'

def dataDownload (url: str):
    respuesta = requests.get(url, stream=True)
    
    if respuesta.status_code == 200:
        with open(fileName, 'wb') as descarga:
            descarga.write(respuesta.raw.read())
    else:
        raise Exception(f"Error al descargar los datos: {respuesta.text}")


def limpiarUnPoco(df: pd.DataFrame) -> pd.DataFrame:
    dfLimpio = df.drop('incident_id', axis=1) #Prefiero los id que les da por defecto el pandas
    return dfLimpio


def main():
        
    URL = "https://github.com/jamesqo/gun-violence-data/raw/master/DATA_01-2013_03-2018.tar.gz"
    dataDownload(URL)

    with tarfile.open(fileName, 'r:*') as tar:
        se_ese_ube = tar.getnames()[0]
        dataFreim = pd.read_csv(tar.extractfile(se_ese_ube))

    dataFrameLimpio = limpiarUnPoco(dataFreim)
    dataFrameLimpio.to_csv('2013-01_2018-03.csv') #Sé que es redundante pero quería probar el método

    print(dataFrameLimpio)


if __name__ == "__main__":
    main()
