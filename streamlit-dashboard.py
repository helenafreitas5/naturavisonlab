import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np
from faker import Faker
import random
import io

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Inicializa Faker para dados fictícios
fake = Faker('pt_BR')

def gerar_dados_tendencias(num_records=100):
    """Gera dados fictícios de tendências de mercado"""
    categorias = ["Perfumaria", "Cosméticos", "Maquiagem", "Skin Care"]
    fontes = ["Google Trends", "Redes Sociais", "Pesquisas de Mercado", "Consultoria Externa"]
    tendencias = ["Crescente", "Estável", "Decrescente"]
    lista = []
    data_inicio = datetime.today() - timedelta(days=365)
    for _ in range(num_records):
        lista.append({
            'Data': (data_inicio + timedelta(days=random.randint(0, 365))).date(),
            'Categoria': random.choice(categorias),
            'Tendência': random.choice(tendencias),
            'Índice': round(random.uniform(0, 100), 2),
            'Fonte': random.choice(fontes),
            'Observações': fake.sentence(nb_words=10)
        })
    return pd.DataFrame(lista)

def gerar_dados_sentimento(num_records=50):
    """Gera dados fictícios de sentimento externo"""
    categorias = ["Perfumaria", "Cosméticos", "Maquiagem", "Skin Care"]
    plataformas = ["Twitter", "Instagram", "Facebook", "YouTube", "Blogs"]
    sentimentos = ["Positivo", "Neutro", "Negativo"]
    lista = []
    data_inicio = datetime.today() - timedelta(days=365)
    for _ in range(num_records):
        lista.append({
            'Data': (data_inicio + timedelta(days=random.randint(0, 365))).date(),
            'Categoria': random.choice(categorias),
            'Plataforma': random.choice(plataformas),
            'Sentimento': random.choice(sentimentos),
            'Volume': random.randint(100, 10000)
        })
    return pd.DataFrame(lista)

def zaia_widget():
    """Exibe o Chatbot da Zaia"""
    widget_html = """
        <div>
            <script>
                window.Widget = {
                    AgentURL: "https://platform.zaia.app/embed/chat/36828",
                };
            </script>
            <script src="https://platform.zaia.app/script/widget-loader.js"></script>
        </div>
    """
    components.html(widget_html, height=700)

# Sidebar - Navegação
st.sidebar.title("Navegação")
selecao = st.sidebar.radio("Escolha uma seção:", [
    "📡 Fontes de Dados", "💬 ChatBot Zaia", "🎯 Estúdio"])

# Fontes de Dados
if selecao == "📡 Fontes de Dados":
    st.title("📡 Fontes de Dados")
    st.subheader("Gerenciamento das fontes de dados ativas")
    st.write("Aqui você pode ativar/desativar fontes de dados para análise.")
    
    fontes_disponiveis = {
        "Google Trends": True,
        "SalesForce": False,
        "Instagram": True,
        "TikTok": False,
        "LinkedIn": False,
        "YouTube": True
    }
    
    for fonte, ativo in fontes_disponiveis.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(fonte, value=ativo)
        with col2:
            if ativo:
                st.success("Ativo")
            else:
                st.warning("Pendente")

# ChatBot Zaia
elif selecao == "💬 ChatBot Zaia":
    st.title("💬 ChatBot Zaia")
    st.subheader("Converse com o assistente de IA da Natura")
    zaia_widget()

# Estúdio
elif selecao == "🎯 Estúdio":
    st.title("🎯 Estúdio")
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Análise", "🌐 Tendências Externas"])
    
    with tab1:
        st.subheader("📊 Dashboard")
        st.write("Gráficos de sentimento e participação de mercado")
        sentiment_data = gerar_dados_sentimento()
        fig_sentiment = px.box(sentiment_data, x='Categoria', y='Volume', color='Categoria', title='Sentimento por Categoria')
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Análise")
        st.write("Relatórios e insights baseados nos dados coletados")
        st.markdown("#### 📑 Relatórios de Performance")
        with st.expander("📊 Análise de Performance"):
            st.write("Resumo do desempenho recente no mercado.")
        with st.expander("💡 Recomendações"):
            st.write("Sugestões estratégicas baseadas na análise de tendências.")
    
    with tab3:
        st.subheader("🌐 Tendências Externas")
        tendencias_df = gerar_dados_tendencias()
        st.dataframe(tendencias_df)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            tendencias_df.to_excel(writer, sheet_name="Tendências_Mercado", index=False)
        output.seek(0)
        st.download_button("📥 Baixar Tendências", data=output, file_name="tendencias_mercado.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Rodapé
st.markdown("---")
st.markdown(f"<div style='text-align: center'><small>Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Powered by Zaia AI</small></div>", unsafe_allow_html=True)
