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
        
        return interest_over_time_df, related_queries
    except Exception as e:
        st.error(f"Erro ao buscar dados do Google Trends: {str(e)}")
        return None, None

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
trends_df, related_queries = get_google_trends_data()

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
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Google Trends", "💬 Assistente IA", "📊 Análise"])

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

# Google Trends Tab
with tab2:
    st.subheader("📈 Análise de Tendências de Busca")
    
    if trends_df is not None:
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
        trends_df_copy = trends_df.copy()
        trends_df_copy.index = pd.to_datetime(trends_df_copy.index)
        trends_df_copy['month'] = trends_df_copy.index.month
        monthly_avg = trends_df_copy.groupby('month').mean()
        
        fig_seasonal = px.line(monthly_avg, 
                             title="Média Mensal de Interesse",
                             labels={'value': 'Interesse Médio', 
                                    'month': 'Mês'},
                             height=300)
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Termos Relacionados
        if related_queries:
            st.subheader("Termos de Busca Relacionados")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Pele Oleosa - Top Buscas Relacionadas")
                if 'pele oleosa' in related_queries:
                    top_queries = related_queries['pele oleosa'].get('top')
                    if isinstance(top_queries, pd.DataFrame):
                        st.dataframe(top_queries.head())
            
            with col2:
                st.write("Pele Seca - Top Buscas Relacionadas")
                if 'pele seca' in related_queries:
                    top_queries = related_queries['pele seca'].get('top')
                    if isinstance(top_queries, pd.DataFrame):
                        st.dataframe(top_queries.head())
    else:
        st.error("Não foi possível carregar os dados do Google Trends")

# Chat Tab
with tab3:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Análise Tab
with tab4:
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
