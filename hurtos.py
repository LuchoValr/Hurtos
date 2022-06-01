import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
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
sex
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
#Grafico de Barras segun sexo
#Enero
sexv_enero=sexv.loc[sexv["FECHA HECHO"].between('2021-01-01', '2021-01-31')]
fsexv1=sns.catplot(data=sexv_enero,x='GENERO',y='CANTIDAD',kind='bar',size=7)
plt.show()
#Febrero
sexv_febrero=sexv.loc[sexv["FECHA HECHO"].between('2021-02-01', '2021-02-28')]
fsexv2=sns.catplot(data=sexv_febrero,x='GENERO',y='CANTIDAD',kind='bar',size=7)
plt.show()
#Marzo
sexv_marzo=sexv.loc[sexv["FECHA HECHO"].between('2021-03-01', '2021-03-31')]
fsexv3=sns.catplot(data=sexv_marzo,x='GENERO',y='CANTIDAD',kind='bar',size=7)
plt.show()
#Grafico de barras segun edad
agev=hur.groupby(by=['FECHA HECHO','EDAD PERSONA']).sum().groupby(level=[0]).cumsum()
agev=agev.reset_index()
#Enero
agev_enero=agev.loc[agev["FECHA HECHO"].between('2021-01-01', '2021-01-31')]
fagev=sns.catplot(data=agev_enero,x='EDAD PERSONA',y='CANTIDAD',kind='bar',size=7)
plt.show()
#Graficos de barras segun armas
wepv=hur.groupby(by=['FECHA HECHO','ARMAS MEDIO']).sum().groupby(level=[0]).cumsum()
wepv=wepv.reset_index()
#Enero
wepv_enero=wepv.loc[wepv["FECHA HECHO"].between('2021-01-01', '2021-01-31')]
fwepv=sns.catplot(data=wepv_enero,x='ARMAS MEDIO',y='CANTIDAD',kind='bar',size=10)
plt.show()
#Graficas relacionando el genero con el arma usada
sex_wep1=hur.filter(['ARMAS MEDIO','GENERO','FECHA HECHO','CANTIDAD'])
#Masculino
sex_wepm=sex_wep1[sex_wep1.GENERO.isin(['MASCULINO'])]
sex_wepm=sex_wepm.groupby(by=['FECHA HECHO','ARMAS MEDIO','GENERO']).sum().groupby(level=[0]).cumsum()
sex_wepm=sex_wepm.reset_index()
#Enero
sex_wep_enerom=sex_wepm.loc[sex_wepm["FECHA HECHO"].between('2021-01-01', '2021-01-31')]
fsex_wepm_enero=sns.catplot(data=sex_wep_enerom,x='ARMAS MEDIO',y='CANTIDAD',kind='bar',size=10)
plt.show()
#Femenino
sex_wepf=sex_wep1[sex_wep1.GENERO.isin(['FEMENINO'])]
sex_wepf=sex_wepf.groupby(by=['FECHA HECHO','ARMAS MEDIO','GENERO']).sum().groupby(level=[0]).cumsum()
sex_wepf=sex_wepf.reset_index()
#Enero
sex_wep_enerof=sex_wepf.loc[sex_wepf["FECHA HECHO"].between('2021-01-01', '2021-01-31')]
fsex_wepf_enero=sns.catplot(data=sex_wep_enerof,x='ARMAS MEDIO',y='CANTIDAD',kind='bar',size=10)
plt.show()



#Grafico de barras totales genero
f=sns.catplot(data=sex,x='GENERO',y='CANTIDAD',kind='bar',size=7)
plt.show()
#Heatmap
import requests
import plotly.offline as pyo
dep2=hur.groupby(by=['DEPARTAMENTO']).sum().groupby(level=[0]).cumsum()
dep=dep2.reset_index()
dep['DEPARTAMENTO']=dep['DEPARTAMENTO'].replace({'ATLÁNTICO':'ATLANTICO','BOLÍVAR':'BOLIVAR','BOYACÁ':'BOYACA','CAQUETÁ':'CAQUETA',
'CÓRDOBA':'CORDOBA','CHOCÓ':'CHOCO','GUAJIRA':'LA GUAJIRA','QUINDÍO':'QUINDIO','VALLE':'VALLE DEL CAUCA',
'GUAINÍA':'GUANIA','VAUPÉS':'VAUPES','SAN ANDRÉS':'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'})
url='https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
col_regions_geo = requests.get(url).json()
fig = px.choropleth_mapbox(data_frame=dep, 
                    geojson=col_regions_geo, 
                    locations='DEPARTAMENTO', # nombre de la columna del Dataframe
                    featureidkey='properties.NOMBRE_DPT',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    color='CANTIDAD', #El color depende de las cantidades
                    color_continuous_scale="Viridis", #greens
                   )
fig.update_layout(mapbox_style="carto-positron",mapbox_zoom=4.2, mapbox_center = {"lat": 4.570868, "lon": -74.2973328},title_text='Hurtos en Colombia del 2021')
fig.show()
pyo.plot(fig, filename = 'C:\\Users\\lucho\\OneDrive\\Documentos\\Proyectos\\Victimas-Crimen\\Hurtos\\mapa_col.html')





