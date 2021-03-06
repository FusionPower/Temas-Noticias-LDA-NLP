#!/usr/bin/env python
# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Analisis de temas de noticas")
st.markdown(" El Universal, Milenio y La Jornada")
st.markdown(" 31 de Enero - 20 de Febrero")


data_="data.csv"

@st.cache(persist=True)
def load_data():
	data = pd.read_csv(data_)
	return data
def print_format(string):
	string=string[2:-2]
	string=string.replace("\\"+"n","""
""")
	string=string.replace("\\"+"xa0","")
	string=string.replace("\\"+"x","""
#""")
	return string


data = load_data()

st.sidebar.title("Visualizaciones:")

st.sidebar.markdown(" ## Mostrar contribución por tema:")
select = st.sidebar.selectbox("Tipo de visualización:",["Gráfica de barras", "Gráfica de pay" ], key="1")

names={0:"tema0",1:"tema1",2:"tema2",3:"tema3",4:"tema4",5:"tema5",6:"tema6",7:"tema7",8:"Tema Principal",9:"Contribucion",10:"Palabras Clave",11:"Texto Normalizado",12:"Texto Original"}


df_contribution =  data[["tema0","tema1","tema2","tema3","tema4","tema5","tema6","tema7"]].sum(axis=0)

data_presencia = data[["Tema Principal"]].value_counts().sort_index()
mostrar_presencia= pd.DataFrame({"Tema":[0,1,2,3,4,5,6,7],"#Documentos":data_presencia.values,"Presencia en los textos": df_contribution.values})



if st.sidebar.checkbox("#Documentos con tema dominante", True):
	st.markdown("## Numero de documentos con tema dominante x:")
	if select == "Gráfica de barras":
		fig = px.bar (mostrar_presencia, x="Tema", y="#Documentos",color = "Tema",range_y=[0,500])
		st.plotly_chart(fig)
	else:
		fig = px.pie (mostrar_presencia, names="Tema", values="#Documentos")
		st.plotly_chart(fig)
	
if st.sidebar.checkbox("Contribucion al corpus por tema", True):
	st.markdown("## Contribución por tema al corpus:")
	if select == "Gráfica de barras":
		fig2 = px.bar (mostrar_presencia, x="Tema", y="Presencia en los textos",color = "Tema",range_y=[0,500])
		st.plotly_chart(fig2)
	else:
		fig2 = px.pie(mostrar_presencia, names="Tema", values="Presencia en los textos")
		st.plotly_chart(fig2)
		
st.sidebar.markdown(" ## Mostrar noticia por tema dominante:")
noticia_aleatoria = st.sidebar.radio("Tema", ("tema0","tema1","tema2","tema3","tema4","tema5","tema6","tema7"))
st.markdown("## %s%s"%("T",noticia_aleatoria[1:]))

nota=data[data["Tema Principal"]== int(noticia_aleatoria[-1])][["tema0","tema1","tema2","tema3","tema4","tema5","tema6","tema7","Texto Original"]].sample(n=1)

string=nota[["Texto Original"]].iat[0,0]


st.markdown(print_format(string))


if st.sidebar.checkbox("Mostrar distribución de temas", True):
	distribucion=nota[["tema0","tema1","tema2","tema3","tema4","tema5","tema6","tema7"]].sum(axis=0)
	distribucion= pd.DataFrame({"Tema":[0,1,2,3,4,5,6,7],"Distribución":distribucion.values})
	
	fig3 = px.pie(distribucion, names="Tema", values="Distribución")
	st.plotly_chart(fig3)
