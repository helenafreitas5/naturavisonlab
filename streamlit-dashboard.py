import streamlit as st
import pandas as pd
from notion_client import Client
import requests
from datetime import datetime
import plotly.express as px

# Configuração
st.set_page_config(layout="wide", page_title="BABI Monitor")

# APIs
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
ZAIA_API_KEY = st.secrets["ZAIA_API_KEY"]
MAKE_WEBHOOK = st.secrets["MAKE_WEBHOOK"]

notion = Client(auth=NOTION_TOKEN)

# ZAIA API Functions
def analyze_with_zaia(text):
    headers = {"Authorization": f"Bearer {ZAIA_API_KEY}"}
    response = requests.post(
        "https://api.zaia.ai/analyze",
        headers=headers,
        json={"text": text}
    )
    return response.json()

def get_notion_updates():
    results = notion.databases.query(
        database_id="seu_database_id",
        sorts=[{"property": "Date", "direction": "descending"}]
    )
    return results.get("results", [])

# Interface
st.sidebar.title("BABI Monitor")
menu = st.sidebar.selectbox(
    "Menu", 
    ["Dashboard", "Monitoramento", "Análise ZAIA", "Territórios", "Taxonomia"]
)

if menu == "Dashboard":
    st.title("Dashboard BABI")
    
    # KPIs
    kpis = st.columns(4)
    kpis[0].metric("Notícias Analisadas", "45")
    kpis[1].metric("Ações Ninja", "7")
    kpis[2].metric("Alertas ZAIA", "3", "+2")
    kpis[3].metric("Insights Gerados", "28")

    # Análise ZAIA
    st.subheader("Últimos Insights ZAIA")
    with st.expander("Ver Análises"):
        st.json({
            "market_trends": ["Trend 1", "Trend 2"],
            "competitor_moves": ["Move 1", "Move 2"],
            "opportunities": ["Opp 1", "Opp 2"]
        })

elif menu == "Monitoramento":
    st.title("Monitoramento de Notícias")
    
    # Filtros
    col1, col2 = st.columns(2)
    relevancia = col1.selectbox("Relevância", ["Todos", "BAU", "Bomba", "Ninja"])
    territorio = col2.selectbox("Território", ["Todos", "Digital", "Sustentabilidade"])
    
    # Feed de Notícias com Análise ZAIA
    st.subheader("Feed de Notícias")
    noticias = get_notion_updates()
    
    for noticia in noticias:
        with st.expander(f"{noticia.get('title', 'Notícia')}"):
            if st.button("Analisar com ZAIA", key=noticia['id']):
                analysis = analyze_with_zaia(noticia.get('text', ''))
                st.json(analysis)

elif menu == "Análise ZAIA":
    st.title("Análise ZAIA")
    
    # Input para análise
    text_input = st.text_area("Digite o texto para análise")
    if st.button("Analisar"):
        with st.spinner("ZAIA está analisando..."):
            analysis = analyze_with_zaia(text_input)
            
            st.subheader("Resultados")
            cols = st.columns(3)
            cols[0].metric("Relevância", analysis.get("relevance", "N/A"))
            cols[1].metric("Sentimento", analysis.get("sentiment", "N/A"))
            cols[2].metric("Prioridade", analysis.get("priority", "N/A"))
            
            st.json(analysis)

elif menu == "Territórios":
    st.title("Mapa de Territórios")
    
    # Visualização de territórios com insights ZAIA
    territorio_data = pd.DataFrame({
        'Território': ['Digital', 'Sustentabilidade', 'Inovação'],
        'Ações': [15, 12, 8],
        'Score_ZAIA': [0.8, 0.6, 0.9]
    })
    
    fig = px.scatter(territorio_data, 
                    x='Ações', 
                    y='Score_ZAIA',
                    size='Ações',
                    text='Território',
                    title='Análise de Territórios por ZAIA')
    st.plotly_chart(fig)

elif menu == "Taxonomia":
    st.title("Taxonomia Dinâmica")
    
    # Taxonomia gerada pelo ZAIA
    st.subheader("Palavras-chave por Território")
    
    taxonomia = {
        'Digital': ['e-commerce', 'mobile', 'app'],
        'Sustentabilidade': ['reciclagem', 'verde', 'eco'],
        'Inovação': ['AI', 'blockchain', 'IoT']
    }
    
    for categoria, palavras in taxonomia.items():
        with st.expander(categoria):
            st.write(", ".join(palavras))
            if st.button(f"Atualizar {categoria} com ZAIA"):
                st.info("Atualizando taxonomia...")
                # Integração com ZAIA para atualizar palavras-chave

# Webhook para MAKE
def send_to_make(data):
    requests.post(MAKE_WEBHOOK, json=data)

# Footer
st.markdown("---")
st.markdown("Powered by ZAIA AI & MAKE")
