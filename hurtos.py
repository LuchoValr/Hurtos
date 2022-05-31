import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
#Lectura de archivo
archivo='C:\\Users\\lucho\\OneDrive\\Documentos\\Proyectos\\Victimas-Crimen\\Hurtos\\hurto_a_personas_1.xlsx'
hur = pd.read_excel(archivo)
hur=hur.drop([0,1,2,3,4,5,6,7,8,89249,89250,89251,89252,89253])
hur=hur.drop(['Unnamed: 6'],axis=1)
hur=hur.rename(columns={'MINISTERIO DE DEFENSA NACIONAL':'ARMAS MEDIO','Unnamed: 1':'DEPARTAMENTO','Unnamed: 2':'MUNICIPIO','Unnamed: 3':'FECHA HECHO','Unnamed: 4':'GENERO','Unnamed: 5':'EDAD PERSONA','Unnamed: 7':'CANTIDAD'})
#Limpieza
for col in hur.columns:
  print(col)
  print(hur[col].unique())
  print(hur[col].dtypes)
  print('---'*10)

hur.info()

sex=hur.groupby(by=['GENERO']).sum().groupby(level=[0]).cumsum()
sex=sex.reset_index()
age=hur.groupby(by=['EDAD PERSONA']).sum().groupby(level=[0]).cumsum()
age
wep=hur.groupby(by=['ARMAS MEDIO']).sum().groupby(level=[0]).cumsum()
wep
date=hur.groupby(by=['FECHA HECHO']).sum().groupby(level=[0]).cumsum()
date
#En edad y sexo solo 1 en cada no reportado y en armas 1821 no reportadas
#Visualizacion
sexv=hur.groupby(by=['FECHA HECHO','GENERO']).sum().groupby(level=[0]).cumsum()
sexv=sexv.reset_index()
#Series de tiempo
#Enero
sexv_enero=sexv.loc[sexv["FECHA HECHO"].between('2021-01-01', '2021-01-31')]
sexv_enero=sexv_enero.pivot_table(index='FECHA HECHO',columns='GENERO',values='CANTIDAD')
f2=sexv_enero[['FEMENINO','MASCULINO']].plot()
plt.show()
#Grafico de barras
f=sns.catplot(data=sex,x='GENERO',y='CANTIDAD',kind='bar',size=7)
plt.show()
#Heatmap
import geopandas as gpd
import requests
dep1=hur.groupby(by=['DEPARTAMENTO']).sum().groupby(level=[0]).cumsum()
dep=dep1.reset_index()
dep['DEPARTAMENTO']=dep['DEPARTAMENTO'].replace({'ATLÁNTICO':'ATLANTICO','BOLÍVAR':'BOLIVAR','BOYACÁ':'BOYACA','CAQUETÁ':'CAQUETA',
'CÓRDOBA':'CORDOBA','CHOCÓ':'CHOCO','HUILA':'Huila','GUAJIRA':'LA GUAJIRA','QUINDÍO':'QUINDIO','VALLE':'VALLE DEL CAUCA',
'GUAINÍA':'GUANIA','VAUPÉS':'VAUPES','SAN ANDRÉS':'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'})
url='https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
col_regions_geo = requests.get(url).json()

fig = px.choropleth(data_frame=dep, 
                    geojson=col_regions_geo, 
                    locations='DEPARTAMENTO', # nombre de la columna del Dataframe
                    featureidkey='properties.NOMBRE_DPT',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    color='CANTIDAD', #El color depende de las cantidades
                    color_continuous_scale="burg", #greens
                   )
fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations",mapbox_zoom=3.4,mapbox_center = {"lat": 4.570868, "lon": -74.2973328})
fig.show()





