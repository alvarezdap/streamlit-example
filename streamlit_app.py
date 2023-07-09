import streamlit as st

from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import pandas as pd

import plotly.express as px

st.markdown('Perritos perdidos')
st.markdown('''La suposición de que los animales no tienen derechos y la ilusión de que nuestro trato hacia ellos no tiene ninguna 
            importancia moral es un ejemplo positivamente escandaloso de grosería y barbarie occidental. La compasión universal es 
            la única garantía de la moralidad.
            ''')
st.title('Arthur Schopenhauer')
api_token=st.secrets['mapbox']

# Create a connection object.
def objeto_conexion():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(st.secrets['gcp_service_account'],scopes=scope)
    client =Client(scope=scope,creds=credentials)
    spreadsheetname='direcciones_perritos'
    spread=Spread(spreadsheetname,client=client)
    sh=client.open(spreadsheetname)
    worksheet_list=sh.worksheets()
    return spreadsheetname, sh, spread, worksheet_list

def load_the_spreadsheet(spreadsheetname):
    worksheet =sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def plotea_mapa():
    global api_token
    mapa=load_the_spreadsheet("Hoja 1")
    fig=px.scatter_mapbox(mapa,
                              lat='Lat',
                              lon='Lon',
                              hover_name='Nombre',
                              hover_data=['Especie','Provincia','Ciudad'],
                              color=mapa['Especie'],
                              size_max=1000000,
                              zoom=8,
                              mapbox_style='stamen-toner'
                              )
    
    fig.update_layout(autosize=True,hovermode='closest',mapbox=dict(accesstoken=api_token['api_token'],bearing=0,center=dict(lat=-1.4386338911881158,lon=-78.34621847043944),pitch=0,zoom=5))
    fig.update_traces(marker=dict(size=10))                                                                                  
    fig.update_layout(scattermode='group',margin={'r':0,'t':0,'l':0,'b':0})

    return st.plotly_chart(fig)

spreadsheetname, sh, spread, worksheet_list = objeto_conexion()
plotea_mapa()

def anadir_mascotas():
    option = st.selectbox('Mascota',('Perro','Gato'))

anadir_mascotas()
