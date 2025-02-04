import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Widget HTML da Zaia
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

# Dados mockados
@st.cache_data
def load_mock_data():
    benchmark_data = pd.DataFrame([
        {"category": "Skincare", "natura": 85, "avon": 75, "boticario": 80},
        {"category": "Makeup", "natura": 78, "avon": 82, "boticario": 85},
        {"category": "Perfumes", "natura": 90, "avon": 85, "boticario": 88}
    ])
    
    trends_data = pd.DataFrame([
        {"month": "Jan", "skincare": 65, "makeup": 45},
        {"month": "Feb", "skincare": 70, "makeup": 52},
        {"month": "Mar", "skincare": 85, "makeup": 58}
    ])
    
    market_data = pd.DataFrame([
        {"name": "Natura", "value": 35},
        {"name": "Avon", "value": 25},
        {"name": "Boticário", "value": 20}
    ])
    
    performance_data = pd.DataFrame([
        {"category": "Skincare", "atual": 92, "meta": 85},
        {"category": "Makeup", "atual": 78, "meta": 80}
    ])
    
    return benchmark_data, trends_data, market_data, performance_data

# Carrega dados
benchmark_data, trends_data, market_data, performance_data = load_mock_data()

# Header
col1, col2, col3 = st.columns([2,6,2])
with col2:
    st.title("🎯 Plataforma IC Natura")

# Sidebar - Fontes de Dados
with st.sidebar:
    st.header("Fontes de Dados")
    
    # Busca
    search = st.text_input("🔍 Buscar fontes...", "")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔍 Filtrar")
    with col2:
        st.button("📅 Data")
    
    # Lista de fontes
    st.subheader("Fontes Disponíveis")
    
    # Dados de Mercado
    st.markdown("#### 📊 Dados de Mercado")
    market_sources = {
        "Google Trends": True,
        "SalesForce": False,
    }
    
    for source, active in market_sources.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(source, value=active)
        with col2:
            if active:
                st.success("ativo")
            else:
                st.warning("pendente")
    
    # Redes Sociais
    st.markdown("#### 📱 Redes Sociais")
    social_sources = {
        "Instagram": False,
        "TikTok": False,
        "LinkedIn": False,
        "YouTube": False
    }
    
    for source, active in social_sources.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(source, value=active)
        with col2:
            if active:
                st.success("ativo")
            else:
                st.warning("pendente")

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Assistente IA", "📈 Análise"])

# Dashboard Tab
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tendências de Mercado")
        fig_trends = px.line(trends_data, x="month", y=["skincare", "makeup"],
                           title="Evolução de Categorias")
        st.plotly_chart(fig_trends, use_container_width=True)
        
        st.subheader("Market Share")
        fig_market = px.pie(market_data, values="value", names="name",
                          title="Participação de Mercado")
        st.plotly_chart(fig_market, use_container_width=True)
    
    with col2:
        st.subheader("Performance vs Meta")
        fig_perf = px.bar(performance_data, x="category", y=["atual", "meta"],
                         barmode="group", title="Performance por Categoria")
        st.plotly_chart(fig_perf, use_container_width=True)
        
        st.subheader("Benchmark Competitivo")
        fig_bench = px.bar(benchmark_data, x="category", 
                          y=["natura", "avon", "boticario"],
                          title="Comparativo com Concorrentes")
        st.plotly_chart(fig_bench, use_container_width=True)

# Chat Tab com widget da Zaia
with tab2:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Análise Tab
with tab3:
    st.subheader("Relatório Automático")
    
    with st.expander("📊 Análise de Performance"):
        st.write("Análise de performance do último trimestre:")
        st.write("• Crescimento em Skincare: +15% vs trimestre anterior")
        st.write("• Oportunidade em Makeup: -2% vs meta estabelecida")
        st.write("• Destaque para produtos coreanos: +45% em buscas")
    
    with st.expander("💡 Recomendações"):
        st.write("• Aumentar investimento em linha de Skincare")
        st.write("• Revisar estratégia de Makeup")
        st.write("• Explorar parcerias com marcas coreanas")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Exportar Relatório"):
            st.success("Relatório exportado com sucesso!")
    with col2:
        if st.button("📧 Compartilhar"):
            st.success("Link de compartilhamento gerado!")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center'>
        <small>Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')} | 
        Powered by Zaia AI</small>
    </div>
    """,
    unsafe_allow_html=True)
