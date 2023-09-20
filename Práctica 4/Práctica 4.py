import pandas as pd
import plotly as pt
import plotly.graph_objects as go


def main():
    GVDdf = pd.read_csv("../Práctica 2/2013-01_2018-03.csv", index_col=0)
        
    GVDdf['IncidentInfo'] = GVDdf.date + '\n' + GVDdf.address + '\n' + GVDdf.notes 


    fig = go.Figure(data=go.Scattergeo(
        lon = GVDdf.longitude,
        lat = GVDdf.latitude,
        text = GVDdf['IncidentInfo'],
        mode = 'markers',
        ))

    fig.update_layout(
        title = 'Gun Violence Incidents from 2013 to 2018 <br>(Hover for incident info)',
        geo_scope='usa',
    )
    
    pt.offline.plot(fig, filename="mapaCasosINUTIL.html")
    fig.write_image("mapaCasosINUTIL.png")

if __name__ == "__main__":
    main()
