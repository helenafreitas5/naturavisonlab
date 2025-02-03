import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Dados mockados (os mesmos do React)
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
    sources = {
        "Google Trends": True,
        "Social Media": True,
        "Market Reports": False,
        "News Feed": True
    }
    
    for source, active in sources.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(source, value=active)
        with col2:
            if active:
                st.success("ativo")
            else:
                st.warning("pendente")

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Chat", "📈 Análise"])

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

# Chat Tab
with tab2:
    st.subheader("Chat de Análise")
    
    # Mensagens do sistema
    st.info("✓ Fontes conectadas: Google Trends, Social Media")
    st.success("Identifiquei tendências relevantes do setor de beleza. A busca por 'skincare coreano' aumentou 45% no último trimestre.")
    
    # Input do usuário
    user_input = st.text_input("Digite sua pergunta ou comando de análise...")
    if st.button("Enviar"):
        st.write("Você: " + user_input)

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
st.markdown("*Dados atualizados em: {}*".format(datetime.now().strftime("%d/%m/%Y %H:%M")))
