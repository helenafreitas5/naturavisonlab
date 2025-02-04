import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from pytrends.request import TrendReq
import time

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Função melhorada para Google Trends
@st.cache_data(ttl=3600)
def get_google_trends_data():
    try:
        pytrends = TrendReq(hl='pt-BR', timeout=(10,25), retries=2, backoff_factor=0.1)
        
        # Keywords organizadas por categoria
        categories = {
            'Tipos de Pele': ['pele oleosa', 'pele seca', 'pele mista'],
            'Tratamentos': ['skincare', 'anti idade', 'hidratação'],
            'Produtos': ['natura', 'avon', 'boticario']
        }
        
        results = {}
        
        for category, keywords in categories.items():
            # Evitar rate limiting
            time.sleep(1)
            
            # Interest Over Time
            pytrends.build_payload(
                keywords,
                cat=0,
                timeframe='today 12-m',
                geo='BR',
                gprop=''
            )
            
            # Dados de interesse ao longo do tempo
            interest_over_time = pytrends.interest_over_time()
            if 'isPartial' in interest_over_time.columns:
                interest_over_time = interest_over_time.drop('isPartial', axis=1)
            
            # Interesse por região
            interest_by_region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
            
            # Tópicos relacionados
            related_topics = pytrends.related_topics()
            
            # Consultas relacionadas
            related_queries = pytrends.related_queries()
            
            results[category] = {
                'over_time': interest_over_time,
                'by_region': interest_by_region,
                'related_topics': related_topics,
                'related_queries': related_queries
            }
            
        return results
    
    except Exception as e:
        st.error(f"Erro ao buscar dados do Google Trends: {str(e)}")
        return None

# Widget da Zaia
def zaia_widget():
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

# Carregar dados
trends_data = get_google_trends_data()

# Interface principal
st.title("🎯 Plataforma IC Natura")

# Sidebar
with st.sidebar:
    st.header("Configurações de Análise")
    
    if trends_data:
        selected_category = st.selectbox(
            "Categoria",
            options=list(trends_data.keys()),
            key='category_selector'
        )
        
        time_range = st.select_slider(
            "Período",
            options=['1 mês', '3 meses', '6 meses', '12 meses'],
            value='3 meses',
            key='time_range_selector'
        )

# Tabs principais
tab1, tab2, tab3 = st.tabs(["📊 Tendências", "💬 Assistente IA", "📈 Análise Regional"])

# Tab de Tendências
with tab1:
    if trends_data and selected_category in trends_data:
        data = trends_data[selected_category]
        
        # Gráfico de tendências
        st.subheader(f"Tendências de Busca - {selected_category}")
        fig = px.line(
            data['over_time'],
            title=f"Interesse ao longo do tempo - {selected_category}",
            labels={'value': 'Interesse de Busca', 'date': 'Data'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas de comparação
        col1, col2, col3 = st.columns(3)
        
        for idx, keyword in enumerate(data['over_time'].columns):
            with col1 if idx % 3 == 0 else col2 if idx % 3 == 1 else col3:
                current = data['over_time'][keyword].iloc[-1]
                previous = data['over_time'][keyword].iloc[-2]
                delta = ((current - previous) / previous * 100) if previous != 0 else 0
                
                st.metric(
                    label=keyword,
                    value=f"{current:.0f}",
                    delta=f"{delta:.1f}%"
                )
        
        # Queries relacionadas
        st.subheader("Buscas Relacionadas")
        cols = st.columns(len(data['related_queries']))
        
        for (keyword, queries), col in zip(data['related_queries'].items(), cols):
            with col:
                st.write(f"**{keyword}**")
                if queries['top'] is not None:
                    st.dataframe(queries['top'].head())
                else:
                    st.write("Sem dados suficientes")

# Tab do Assistente
with tab2:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Tab de Análise Regional
with tab3:
    if trends_data and selected_category in trends_data:
        st.subheader(f"Análise Regional - {selected_category}")
        
        # Mapa de calor por região
        fig = px.choropleth(
            data['by_region'],
            locations=data['by_region'].index,
            scope="south america",
            color=data['by_region'].columns[0],
            center={"lat": -14.2350, "lon": -51.9253},
            title=f"Interesse por Região - {data['by_region'].columns[0]}"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de dados regionais
        st.subheader("Dados por Região")
        st.dataframe(data['by_region'])

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center'>
        <small>Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')} | 
        Powered by Zaia AI</small>
    </div>
    """,
    unsafe_allow_html=True
)
