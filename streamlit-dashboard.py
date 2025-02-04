import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np

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

# Dados simulados baseados em tendências reais
@st.cache_data
def load_mock_data():
    # Dados de busca por tipo de pele (simulando dados do Google Trends)
    dates = pd.date_range(start='2024-01-01', end='2024-02-04', freq='D')
    
    # Simulando dados com sazonalidade e tendências
    np.random.seed(42)  # Para reprodutibilidade
    
    # Tendência de pele oleosa (maior no verão)
    base_oleosa = 65 + np.sin(np.linspace(0, np.pi, len(dates))) * 20
    noise_oleosa = np.random.normal(0, 5, len(dates))
    pele_oleosa = base_oleosa + noise_oleosa
    
    # Tendência de pele seca (maior no inverno)
    base_seca = 45 + np.sin(np.linspace(0, np.pi, len(dates))) * 15
    noise_seca = np.random.normal(0, 5, len(dates))
    pele_seca = base_seca + noise_seca
    
    skin_trends = pd.DataFrame({
        'data': dates,
        'pele_oleosa': pele_oleosa,
        'pele_seca': pele_seca
    })
    
    return skin_trends

# Carrega dados
skin_trends = load_mock_data()

# Header
st.title("🎯 Plataforma IC Natura")

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Assistente IA", "📈 Análise"])

# Dashboard Tab
with tab1:
    # Diferença entre Pele Oleosa e Pele Seca
    st.subheader("Tendências de Busca: Pele Oleosa vs Pele Seca (Brasil, 2024)")
    
    # Gráfico principal de tendências
    fig_trends = go.Figure()
    
    # Adiciona linhas para cada tipo de pele
    fig_trends.add_trace(
        go.Scatter(
            x=skin_trends['data'],
            y=skin_trends['pele_oleosa'],
            name="Pele Oleosa",
            line=dict(color="#FF6B6B", width=2),
            fill='tonexty'
        )
    )
    
    fig_trends.add_trace(
        go.Scatter(
            x=skin_trends['data'],
            y=skin_trends['pele_seca'],
            name="Pele Seca",
            line=dict(color="#4ECDC4", width=2),
            fill='tonexty'
        )
    )
    
    # Configuração do layout
    fig_trends.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        height=400,
        xaxis=dict(
            title="Data",
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title="Volume de Busca",
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Métricas e Insights
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        media_oleosa = skin_trends['pele_oleosa'].mean()
        st.metric(
            "Média Pele Oleosa",
            f"{media_oleosa:.1f}",
            f"{skin_trends['pele_oleosa'].iloc[-1] - media_oleosa:.1f}"
        )
    
    with col2:
        media_seca = skin_trends['pele_seca'].mean()
        st.metric(
            "Média Pele Seca",
            f"{media_seca:.1f}",
            f"{skin_trends['pele_seca'].iloc[-1] - media_seca:.1f}"
        )
    
    with col3:
        razao = media_oleosa / media_seca
        st.metric(
            "Razão Oleosa/Seca",
            f"{razao:.2f}x"
        )
    
    with col4:
        correlacao = skin_trends['pele_oleosa'].corr(skin_trends['pele_seca'])
        st.metric(
            "Correlação",
            f"{correlacao:.2f}"
        )
    
    # Insights automáticos
    st.subheader("💡 Insights")
    
    with st.expander("Ver Análise Detalhada"):
        st.write("""
        **Principais Observações:**
        - O interesse por pele oleosa é consistentemente maior que pele seca no Brasil
        - Há uma correlação sazonal clara entre os tipos de pele
        - O volume de buscas por pele oleosa é em média {:.1f}x maior que pele seca
        - Os picos de busca coincidem com mudanças de estação
        
        **Oportunidades:**
        - Desenvolver produtos específicos para pele oleosa
        - Criar conteúdo educativo sobre cuidados com pele oleosa
        - Planejar campanhas sazonais alinhadas com as tendências de busca
        """.format(razao))

# Chat Tab com widget da Zaia
with tab2:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Análise Tab
with tab3:
    st.subheader("Relatório Automático")
    
    with st.expander("📊 Análise de Performance"):
        st.write("Análise de performance do último trimestre:")
        st.write("• Volume de buscas por pele oleosa 30% maior que a média histórica")
        st.write("• Tendência de crescimento nas buscas por cuidados específicos")
        st.write("• Oportunidade de mercado para produtos de controle de oleosidade")
    
    with st.expander("💡 Recomendações"):
        st.write("• Desenvolver linha específica para pele oleosa")
        st.write("• Criar conteúdo educativo sobre cuidados com pele")
        st.write("• Planejar campanhas sazonais")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Exportar Relatório"):
            st.success("Relatório exportado com sucesso!")
    with col2:
        if st.button("📧 Compartilhar"):
            st.success("Link de compartilhamento gerado!")

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
