import pandas as pd
archivo = 'hurto_a_personas_1.xlsx'
hur = pd.read_excel(archivo)
hur = hur.drop([0,1,2,3,4,5,6,7,8,89249,89250,89251,89252,89253])
hur = hur.rename(columns={'MINISTERIO DE DEFENSA NACIONAL':'ARMAS MEDIO','Unnamed: 1':'DEPARTAMENTO','Unnamed: 2':'MUNICIPIO','Unnamed: 3':'FECHA HECHO','Unnamed: 4':'GENERO','Unnamed: 5':'*AGRUPA EDAD PERSONA','Unnamed: 7':'CANTIDAD'})


