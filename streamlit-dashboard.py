import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from pytrends.request import TrendReq

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Configuração do Google Trends
@st.cache_data(ttl=3600)  # Cache por 1 hora
def get_google_trends_data():
    try:
        pytrends = TrendReq(hl='pt-BR')
        kw_list = ["pele oleosa", "pele seca"]
        
        # Últimos 5 anos
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='BR')
        interest_over_time_df = pytrends.interest_over_time()
        
        # Remover coluna isPartial
        if 'isPartial' in interest_over_time_df.columns:
            interest_over_time_df = interest_over_time_df.drop('isPartial', axis=1)
            
        # Pegar dados relacionados
        related_queries = pytrends.related_queries()
        
        return {
            'trends': interest_over_time_df,
            'related_queries': related_queries
        }
    except Exception as e:
        st.error(f"Erro ao buscar dados do Google Trends: {str(e)}")
        return None

# [Resto do código do widget da Zaia permanece igual]

# Dados mockados
@st.cache_data
def load_mock_data():
    # [Código existente permanece igual]
    pass

# Carrega dados
benchmark_data, trends_data, market_data, performance_data = load_mock_data()
google_trends_data = get_google_trends_data()

# Header e Sidebar permanecem iguais

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Google Trends", "💬 Assistente IA", "📊 Análise"])

# Dashboard Tab permanece igual
with tab1:
    # [Código existente permanece igual]
    pass

# Nova Tab de Google Trends
with tab2:
    st.subheader("📈 Análise de Tendências de Busca")
    
    if google_trends_data and 'trends' in google_trends_data:
        trends_df = google_trends_data['trends']
        
        # Gráfico de tendências ao longo do tempo
        fig_time = px.line(trends_df, 
                          title="Interesse ao Longo do Tempo",
                          labels={'value': 'Interesse de Busca', 
                                 'date': 'Data'},
                          height=400)
        st.plotly_chart(fig_time, use_container_width=True)
        
        # Métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Média de Interesse - Pele Oleosa",
                value=f"{trends_df['pele oleosa'].mean():.1f}%",
                delta=f"{trends_df['pele oleosa'].iloc[-1] - trends_df['pele oleosa'].iloc[-2]:.1f}%"
            )
        with col2:
            st.metric(
                label="Média de Interesse - Pele Seca",
                value=f"{trends_df['pele seca'].mean():.1f}%",
                delta=f"{trends_df['pele seca'].iloc[-1] - trends_df['pele seca'].iloc[-2]:.1f}%"
            )
        
        # Análise de Sazonalidade
        st.subheader("Análise de Sazonalidade")
        trends_df['month'] = trends_df.index.month
        monthly_avg = trends_df.groupby('month').mean()
        
        fig_seasonal = px.line(monthly_avg, 
                             title="Média Mensal de Interesse",
                             labels={'value': 'Interesse Médio', 
                                    'month': 'Mês'},
                             height=300)
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Termos Relacionados
        if google_trends_data['related_queries']:
            st.subheader("Termos de Busca Relacionados")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Pele Oleosa - Top Buscas Relacionadas")
                if 'pele oleosa' in google_trends_data['related_queries']:
                    top_queries = google_trends_data['related_queries']['pele oleosa']['top']
                    if isinstance(top_queries, pd.DataFrame):
                        st.dataframe(top_queries.head())
            
            with col2:
                st.write("Pele Seca - Top Buscas Relacionadas")
                if 'pele seca' in google_trends_data['related_queries']:
                    top_queries = google_trends_data['related_queries']['pele seca']['top']
                    if isinstance(top_queries, pd.DataFrame):
                        st.dataframe(top_queries.head())
    else:
        st.error("Não foi possível carregar os dados do Google Trends")

# Tab do Chat com Zaia permanece igual
with tab3:
    st.subheader("💬 Chat com Assistente Natura")
    # [Código do widget da Zaia permanece igual]
    pass

# Tab de Análise
with tab4:
    st.subheader("Relatório Automático")
    # [Código existente permanece igual]
    pass

# Footer permanece igual
