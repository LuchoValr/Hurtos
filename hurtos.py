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
import folium
import requests
dep=hur.groupby(by=['DEPARTAMENTO']).sum().groupby(level=[0]).cumsum()
dep
map_col=gpd.read_file('C:\\Users\\lucho\\OneDrive\\Documentos\\Proyectos\\Victimas-Crimen\\Hurtos\\Departamentos202205_shp\\departamentos.shp')
map_col = map_col.drop(columns=['OBJECTID',	'DeCodigo',	'DeNorma','SHAPE_Area',	'SHAPE_Leng'])
map_col=map_col.drop(columns=['DeArea'])
map_col=map_col.sort_values(by='DeNombre')
map_col
map_col['DeNombre'] = map_col['DeNombre'].replace({'San Andrés Providencia y Santa Catalina':'SAN ANDRÉS',
'Amazonas':'AMAZONAS','Antioquia':'ANTIOQUIA','Arauca':'ARAUCA','Atlántico':'ATLÁNTICO','Bolívar':'BOLÍVAR',
'Boyacá':'BOYACÁ','Caldas':'CALDAS','Caquetá':'CAQUETÁ','Casanare':'CASANARE','Cauca':'CAUCA','Cesar':'CESAR',
'Chocó':'CHOCÓ','Cundinamarca':'CUNDINAMARCA','Córdoba':'CÓRDOBA','Guainía':'GUAINÍA','Guaviare':'GUAVIARE',
'Huila':'HUILA','La Guajira':'GUAJIRA','Magdalena':'MAGDALENA','Meta':'META','Nariño':'NARIÑO','Norte de Santander':'NORTE DE SANTANDER',
'Putumayo':'PUTUMAYO','Quindío':'QUINDÍO','Risaralda':'RISARALDA','Santander':'SANTANDER','Sucre':'SUCRE',
'Tolima':'TOLIMA','Valle del Cauca':'VALLE','Vaupés':'VAUPÉS','Vichada':'VICHADA'})
map_col.index = map_col['DeNombre']
map_col.index.name = 'DEPARTAMENTO'

m = folium.Map(location=[4.5,-74], zoom_start=5.4,min_zoom=4,max_zoom=11)
folium.Choropleth(
    geo_data=map_col.__geo_interface__,
    data=dep,
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Hurtos",
).add_to(m)
map_col





