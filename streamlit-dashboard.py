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

# Dados mockados de ações competitivas
def load_competitive_actions():
    actions = [
        {
            "data": "2024-02-04",
            "acao": "Reinauguração da loja do Center Norte",
            "marca": "O Boticário",
            "categoria": ["Varejo", "BAU"],
            "relevancia": 4,
            "publico": "VD",
            "tipo": "Lançamento",
            "descricao": "Reinauguração com novo conceito de loja",
            "fortalezas": "Experiência do cliente aprimorada, localização estratégica",
            "fraquezas": "Alto investimento necessário",
            "evidencias": "https://exemplo.com/foto1.jpg"
        },
        {
            "data": "2024-02-03",
            "acao": "Campanha Boti Recicla",
            "marca": "O Boticário",
            "categoria": ["Sustentabilidade", "Awareness"],
            "relevancia": 5,
            "publico": "CF",
            "tipo": "Campanha",
            "descricao": "Programa de reciclagem de embalagens",
            "fortalezas": "Engajamento com sustentabilidade, fidelização",
            "fraquezas": "Logística complexa",
            "evidencias": "https://exemplo.com/foto2.jpg"
        }
    ]
    return pd.DataFrame(actions)

# Carrega dados
df_actions = load_competitive_actions()

# Header
st.title("🎯 Plataforma IC Natura")

# Main Content
tabs = st.tabs(["📊 Dashboard", "🔍 Análise Competitiva", "📈 Reports", "💬 Assistente IA"])

# Dashboard Tab
with tabs[0]:
    st.subheader("Visão Geral do Mercado")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ações Monitoradas", "143", "15%")
    with col2:
        st.metric("Campanhas Ativas", "28", "5%")
    with col3:
        st.metric("Novos Lançamentos", "12", "-2%")
    with col4:
        st.metric("Share of Voice", "35%", "3%")

# Análise Competitiva Tab
with tabs[1]:
    st.subheader("Monitoramento de Ações")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        marca_filter = st.multiselect(
            "Marca",
            ["O Boticário", "Avon", "Natura", "Eudora"],
            default=["O Boticário"]
        )
    with col2:
        categoria_filter = st.multiselect(
            "Categoria",
            ["BAU", "Awareness", "Lançamento", "Campanha", "Varejo", "Sustentabilidade"],
            default=["BAU"]
        )
    with col3:
        relevancia_filter = st.slider(
            "Relevância Mínima",
            min_value=1,
            max_value=5,
            value=3
        )
    
    # Tabela de ações
    st.markdown("#### 📋 Ações Monitoradas")
    
    # Função para mostrar ícones de relevância
    def show_relevance(value):
        icons = "⭐" * value
        return icons
    
    # Exibição das ações em cards
    for _, action in df_actions.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                **{action['acao']}**  
                📅 {action['data']} | 🏢 {action['marca']} | 👥 {action['publico']}  
                Relevância: {show_relevance(action['relevancia'])}
                """)
                
                with st.expander("Ver detalhes"):
                    st.markdown("**Descrição:**")
                    st.write(action['descricao'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**💪 Fortalezas:**")
                        st.write(action['fortalezas'])
                    with col2:
                        st.markdown("**⚠️ Fraquezas:**")
                        st.write(action['fraquezas'])
                    
                    st.markdown("**🏷️ Categorias:**")
                    for cat in action['categoria']:
                        st.markdown(f"- {cat}")
            
            st.markdown("---")

# Reports Tab
with tabs[2]:
    st.subheader("Reports e Análises")
    
    # Seletor de período
    period = st.selectbox(
        "Período de Análise",
        ["Últimos 7 dias", "Últimos 30 dias", "Último trimestre", "2024"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de ações por categoria
        st.markdown("#### Ações por Categoria")
        fig_categories = px.bar(
            df_actions['categoria'].explode().value_counts().reset_index(),
            x='index',
            y='categoria',
            title="Distribuição de Ações por Categoria"
        )
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with col2:
        # Gráfico de relevância média por marca
        st.markdown("#### Relevância por Marca")
        fig_relevance = px.box(
            df_actions,
            x='marca',
            y='relevancia',
            title="Distribuição de Relevância por Marca"
        )
        st.plotly_chart(fig_relevance, use_container_width=True)
    
    # Timeline de ações
    st.markdown("#### Timeline de Ações")
    fig_timeline = px.scatter(
        df_actions,
        x='data',
        y='marca',
        size='relevancia',
        color='categoria',
        title="Timeline de Ações Competitivas"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# Chat Tab
with tabs[3]:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Sidebar - Fontes e Filtros
with st.sidebar:
    st.header("Configurações")
    
    # Fontes de Dados
    st.subheader("Fontes de Dados")
    sources = {
        "Google Trends": True,
        "Social Media": True,
        "Market Reports": False,
        "News Feed": True,
        "E-commerce": True
    }
    
    for source, active in sources.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(source, value=active)
        with col2:
            if active:
                st.success("✓")
            else:
                st.warning("×")
    
    # Categorias de Análise
    st.subheader("Categorias de Análise")
    categories = [
        "BAU",
        "Awareness",
        "Perfumaria",
        "Presentes",
        "Lançamento Produto",
        "Redes Sociais",
        "Fashion",
        "Público Jovem",
        "Cabelo"
    ]
    
    for category in categories:
        st.checkbox(category, value=True)

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
