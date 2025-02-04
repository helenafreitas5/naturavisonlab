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

# Dados mockados
@st.cache_data
def load_mock_data():
    # Dados de inovação e lançamentos
    pipeline_data = pd.DataFrame([
        {"empresa": "Boticário", "estagio": "Em Pesquisa", "projetos": 12},
        {"empresa": "Boticário", "estagio": "Em Desenvolvimento", "projetos": 8},
        {"empresa": "Boticário", "estagio": "Em Lançamento", "projetos": 3},
        {"empresa": "Natura", "estagio": "Em Pesquisa", "projetos": 15},
        {"empresa": "Natura", "estagio": "Em Desenvolvimento", "projetos": 6},
        {"empresa": "Natura", "estagio": "Em Lançamento", "projetos": 4},
        {"empresa": "Avon", "estagio": "Em Pesquisa", "projetos": 10},
        {"empresa": "Avon", "estagio": "Em Desenvolvimento", "projetos": 7},
        {"empresa": "Avon", "estagio": "Em Lançamento", "projetos": 2}
    ])
    
    # Dados de tecnologias
    tech_data = pd.DataFrame([
        {"area": "Biotecnologia", "investimento": 85, "crescimento": 15},
        {"area": "IA e Personalização", "investimento": 78, "crescimento": 25},
        {"area": "Nanotecnologia", "investimento": 65, "crescimento": 10},
        {"area": "Sustentabilidade", "investimento": 92, "crescimento": 30},
        {"area": "Embalagens Inteligentes", "investimento": 70, "crescimento": 20}
    ])
    
    return pipeline_data, tech_data

# Carrega dados
pipeline_data, tech_data = load_mock_data()

# Header
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
tabs = st.tabs(["📊 Dashboard", "🔬 Inovação", "💬 Assistente IA", "📈 Studio"])

# Dashboard Tab
with tabs[0]:
    # Métricas Principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Patentes (2024)", "127", "15%")
    with col2:
        st.metric("Projetos Ativos", "43", "8%")
    with col3:
        st.metric("Novas Tecnologias", "28", "12%")
    with col4:
        st.metric("Parcerias", "15", "20%")

    st.markdown("---")
    
    # Radar de Inovação
    st.subheader("🔍 Radar de Inovação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🆕 Últimos Lançamentos")
        launches = [
            {
                "marca": "Boticário",
                "produto": "Linha Botik Skincare Tech",
                "data": "Jan 2024",
                "descrição": "Produtos com tecnologia de microencapsulamento",
                "tipo": "Novo Produto"
            },
            {
                "marca": "Avon",
                "produto": "Power Stay Matte",
                "data": "Jan 2024",
                "descrição": "Base com tecnologia de longa duração",
                "tipo": "Novo Produto"
            },
            {
                "marca": "Natura",
                "produto": "Chronos Biome",
                "data": "Dez 2023",
                "descrição": "Tecnologia de proteção do microbioma",
                "tipo": "Nova Tecnologia"
            }
        ]
        
        for launch in launches:
            with st.container():
                st.markdown(f"""
                **{launch['marca']} - {launch['produto']}**  
                📅 {launch['data']}  
                {launch['descrição']}  
                *Tipo: {launch['tipo']}*
                """)
                st.markdown("---")
    
    with col2:
        st.markdown("#### 🤝 Parcerias e Movimentos Estratégicos")
        partnerships = [
            {
                "empresa": "Boticário",
                "parceiro": "L'Oréal Research",
                "tipo": "P&D",
                "status": "Ativa",
                "descrição": "Desenvolvimento de ativos sustentáveis"
            },
            {
                "empresa": "Natura",
                "parceiro": "MIT Labs",
                "tipo": "Inovação",
                "status": "Em negociação",
                "descrição": "Pesquisa em biotecnologia"
            },
            {
                "empresa": "Avon",
                "parceiro": "Tecnologia K-Beauty",
                "tipo": "Comercial",
                "status": "Ativa",
                "descrição": "Expansão linha coreana"
            }
        ]
        
        for partner in partnerships:
            with st.container():
                col_info, col_status = st.columns([3,1])
                with col_info:
                    st.markdown(f"""
                    **{partner['empresa']} + {partner['parceiro']}**  
                    Tipo: {partner['tipo']}  
                    {partner['descrição']}
                    """)
                with col_status:
                    if partner['status'] == 'Ativa':
                        st.success('Ativa')
                    else:
                        st.warning('Em negociação')
                st.markdown("---")

# Tab de Inovação
with tabs[1]:
    st.subheader("🔬 Análise de Inovação")
    
    # Pipeline de Inovação
    st.markdown("#### 📈 Pipeline de Inovação por Empresa")
    
    fig_pipeline = px.bar(
        pipeline_data,
        x="estagio",
        y="projetos",
        color="empresa",
        title="Pipeline de Inovação por Empresa",
        barmode="group"
    )
    
    st.plotly_chart(fig_pipeline, use_container_width=True)
    
    # Mapa de Tecnologias
    st.markdown("#### 🔍 Mapa de Tecnologias Emergentes")
    
    fig_tech = px.pie(
        tech_data,
        values="investimento",
        names="area",
        title="Distribuição de Investimentos em Tecnologia"
    )
    
    st.plotly_chart(fig_tech, use_container_width=True)
    
    # Monitoramento de Startups
    st.markdown("#### 🚀 Radar de Startups")
    startups = [
        {"nome": "BeautyTech", "foco": "IA para personalização", "interesse": "Alto"},
        {"nome": "EcoPackaging", "foco": "Embalagens sustentáveis", "interesse": "Médio"},
        {"nome": "BioActives", "foco": "Biotecnologia", "interesse": "Alto"}
    ]
    
    for startup in startups:
        with st.container():
            col1, col2 = st.columns([3,1])
            with col1:
                st.markdown(f"""
                **{startup['nome']}**  
                Foco: {startup['foco']}
                """)
            with col2:
                if startup['interesse'] == 'Alto':
                    st.success('Alto Interesse')
                else:
                    st.warning('Médio Interesse')

# Chat Tab
with tabs[2]:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Studio Tab
with tabs[3]:
    st.subheader("Studio")
    
    # Quick Dashboard
    st.markdown("#### 🎯 Dashboard Rápido")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Análise de Mercado"):
            st.metric("Market Share", "35%", "2.5%")
    with col2:
        if st.button("🔬 Pipeline de Inovação"):
            st.metric("Projetos Ativos", "43", "8%")
    with col3:
        if st.button("🚀 Startups"):
            st.metric("Oportunidades", "12", "3")
    
    # Report Generation
    st.markdown("#### 📑 Relatórios")
    with st.expander("📊 Análise de Inovação"):
        st.write("Análise do último trimestre:")
        st.write("• 15 novos projetos iniciados")
        st.write("• 3 parcerias estratégicas estabelecidas")
        st.write("• 5 tecnologias em fase final de desenvolvimento")
    
    with st.expander("💡 Recomendações"):
        st.write("• Acelerar projetos em biotecnologia")
        st.write("• Explorar parcerias com startups")
        st.write("• Investir em personalização")
    
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
