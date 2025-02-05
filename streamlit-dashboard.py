import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import openai

st.set_page_config(layout="wide", page_title="BABI Monitor")

# ZAIA Function (from your previous implementation)
def get_completion(prompt):
    MODEL = "gpt-4"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message["content"]

# Interface
st.sidebar.title("BABI Monitor")
menu = st.sidebar.selectbox(
    "Menu", 
    ["Dashboard", "Monitoramento", "Análise ZAIA", "Territórios", "Taxonomia"]
)

if menu == "Dashboard":
    st.title("Dashboard BABI")
    st.columns(4)[0].metric("Notícias Analisadas", "45")
    st.columns(4)[1].metric("Ações Ninja", "7")
    st.columns(4)[2].metric("Alertas ZAIA", "3")
    st.columns(4)[3].metric("Insights", "28")

elif menu == "Monitoramento":
    st.title("Monitoramento de Notícias")
    relevancia = st.selectbox("Relevância", ["Todos", "BAU", "Bomba", "Ninja"])
    text_input = st.text_area("Cole a notícia para análise")
    
    if st.button("Analisar"):
        response = get_completion(text_input)
        st.write(response)

elif menu == "Análise ZAIA":
    st.title("Análise ZAIA")
    text_input = st.text_area("Digite o texto para análise")
    if st.button("Analisar"):
        with st.spinner("Analisando..."):
            analysis = get_completion(text_input)
            st.write(analysis)

elif menu == "Territórios":
    st.title("Mapa de Territórios")
    territorio_data = pd.DataFrame({
        'Território': ['Digital', 'Sustentabilidade', 'Inovação'],
        'Ações': [15, 12, 8],
        'Score': [0.8, 0.6, 0.9]
    })
    fig = px.scatter(territorio_data, x='Ações', y='Score', text='Território')
    st.plotly_chart(fig)

elif menu == "Taxonomia":
    st.title("Taxonomia Dinâmica")
    taxonomia = {
        'Digital': ['e-commerce', 'mobile', 'app'],
        'Sustentabilidade': ['reciclagem', 'verde', 'eco'],
        'Inovação': ['AI', 'blockchain', 'IoT']
    }
    for categoria, palavras in taxonomia.items():
        with st.expander(categoria):
            st.write(", ".join(palavras))

st.markdown("---")
st.markdown("Powered by ZAIA AI")
