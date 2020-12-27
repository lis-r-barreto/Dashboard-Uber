# import necessary packages
import pandas as pd
import numpy as np
import streamlit as st

DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"


@st.cache
def load_data(nrows=2000):
    # mapa das colunas
    columns = {"Date/Time": "date",
               "Lat": "lat",
               "Lon": "lon"}

    # importar dataframe e limpar os dados
    df = pd.read_csv(DATA_URL, compression="gzip", nrows=nrows)
    df = df.rename(columns=columns)
    df.date = pd.to_datetime(df.date)
    df = df[list(columns.values())]

    return df

# carregar os dados
df = load_data()

# MAIN
st.title("Uber for NYC")
st.markdown(
    f"""
    Dashboard para analise de passageiros Uber na 
    cidade de **New York**.
    
    Carregando {df.shape[0]} linhas de entrada.

    ### Raw Data
    """)

# Raw Data
st.sidebar.header("Configuracoes")
if st.sidebar.checkbox("Mostrar Raw Data"):
    st.write(df)

# mapa
st.subheader("Mapa")
entradas_selecionadas = st.empty()
st.sidebar.subheader("Horario")
hora = st.sidebar.slider("Selecione a hora desejada", 0, 23, 12)
df_filtered = df[df.date.dt.hour == hora]
entradas_selecionadas.text(df_filtered.shape[0])
st.map(df_filtered)

# Histograma
st.subheader("Histograma")
hist = np.histogram(df.date.dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist)





