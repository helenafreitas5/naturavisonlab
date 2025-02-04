import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np
import requests
from datetime import datetime, timedelta
import json

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

# Simulação de dados do LinkedIn e Google Alerts
def get_linkedin_data():
    linkedin_posts = [
        {
            "data": "2024-02-04",
            "empresa": "O Boticário",
            "tipo": "Post",
            "conteudo": "Lançamento da nova linha sustentável",
            "engajamento": 1500,
            "classificacao": "Bomba",
            "relevancia": 5,
            "link": "https://linkedin.com/post1",
            "palavras_chave": ["sustentabilidade", "inovação", "lançamento"]
        },
        {
            "data": "2024-02-03",
            "empresa": "Natura",
            "tipo": "Artigo",
            "conteudo": "Parceria com startup de biotecnologia",
            "engajamento": 800,
            "classificacao": "Ação Ninja",
            "relevancia": 4,
            "link": "https://linkedin.com/post2",
            "palavras_chave": ["biotecnologia", "parceria", "inovação"]
        }
    ]
    return pd.DataFrame(linkedin_posts)

def get_google_alerts():
    alerts = [
        {
            "data": "2024-02-04",
            "fonte": "Portal Cosméticos",
            "titulo": "O Boticário investe em nova fábrica",
            "conteudo": "Investimento de R$ 500 milhões em nova unidade",
            "classificacao": "BAU",
            "relevancia": 3,
            "link": "https://exemplo.com/noticia1",
            "palavras_chave": ["expansão", "investimento", "produção"]
        },
        {
            "data": "2024-02-03",
            "fonte": "Valor Econômico",
            "titulo": "Natura anuncia aquisição",
            "conteudo": "Aquisição de startup de tecnologia",
            "classificacao": "Bomba",
            "relevancia": 5,
            "link": "https://exemplo.com/noticia2",
            "palavras_chave": ["aquisição", "tecnologia", "expansão"]
        }
    ]
    return pd.DataFrame(alerts)

# Taxonomia de palavras-chave
TAXONOMIA = {
    "Inovação": ["tecnologia", "inovação", "pesquisa", "desenvolvimento", "startup"],
    "Sustentabilidade": ["sustentável", "reciclagem", "meio ambiente", "eco-friendly"],
    "Expansão": ["aquisição", "investimento", "nova fábrica", "mercado"],
    "Digital": ["e-commerce", "digital", "online", "app", "plataforma"],
    "Produto": ["lançamento", "linha", "produto", "coleção", "portfólio"]
}

# Classificações
CLASSIFICACOES = {
    "BAU": "Business as Usual - Ações rotineiras",
    "Bomba": "Ações de alto impacto no mercado",
    "Ação Ninja": "Movimentos estratégicos inesperados",
    "Normal": "Ações regulares sem grande impacto"
}

# Carrega dados
linkedin_data = get_linkedin_data()
alerts_data = get_google_alerts()

# Header
st.title("🎯 Plataforma IC Natura")

# Main Content
tabs = st.tabs(["📊 Daily Analysis", "🔍 Monitoramento", "📈 Reports", "💬 Assistente IA"])

# Daily Analysis Tab
with tabs[0]:
    st.subheader("Análise Diária de Movimentos")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        data_filtro = st.date_input(
            "Data da Análise",
            datetime.now()
        )
    with col2:
        classificacao_filtro = st.multiselect(
            "Classificação",
            list(CLASSIFICACOES.keys()),
            default=list(CLASSIFICACOES.keys())
        )
    
    # Movimentos do Dia
    st.markdown("### 📋 Movimentos do Dia")
    
    # LinkedIn
    st.markdown("#### LinkedIn")
    for _, post in linkedin_data.iterrows():
        with st.expander(f"{post['empresa']} - {post['tipo']}"):
            col1, col2 = st.columns([3,1])
            with col1:
                st.markdown(f"**Conteúdo:** {post['conteudo']}")
                st.markdown(f"**Palavras-chave:** {', '.join(post['palavras_chave'])}")
                st.markdown(f"**Engajamento:** {post['engajamento']}")
            with col2:
                if post['classificacao'] == 'Bomba':
                    st.error(post['classificacao'])
                elif post['classificacao'] == 'Ação Ninja':
                    st.warning(post['classificacao'])
                else:
                    st.info(post['classificacao'])
            
            st.markdown(f"[Ver no LinkedIn]({post['link']})")
    
    # Google Alerts
    st.markdown("#### Notícias")
    for _, alert in alerts_data.iterrows():
        with st.expander(f"{alert['titulo']}"):
            col1, col2 = st.columns([3,1])
            with col1:
                st.markdown(f"**Fonte:** {alert['fonte']}")
                st.markdown(f"**Conteúdo:** {alert['conteudo']}")
                st.markdown(f"**Palavras-chave:** {', '.join(alert['palavras_chave'])}")
            with col2:
                if alert['classificacao'] == 'Bomba':
                    st.error(alert['classificacao'])
                elif alert['classificacao'] == 'Ação Ninja':
                    st.warning(alert['classificacao'])
                else:
                    st.info(alert['classificacao'])
            
            st.markdown(f"[Ler mais]({alert['link']})")

# Monitoramento Tab
with tabs[1]:
    st.subheader("Monitoramento de Fontes")
    
    # LinkedIn Insights
    st.markdown("### LinkedIn")
    
    # Gráfico de engajamento
    fig_engagement = px.bar(
        linkedin_data,
        x='empresa',
        y='engajamento',
        color='classificacao',
        title="Engajamento por Empresa"
    )
    st.plotly_chart(fig_engagement, use_container_width=True)
    
    # Análise de palavras-chave
    st.markdown("### Análise de Palavras-chave")
    
    # Criar DataFrame com contagem de palavras-chave
    all_keywords = pd.DataFrame([
        {"palavra": kw, "categoria": cat}
        for cat, keywords in TAXONOMIA.items()
        for kw in keywords
    ])
    
    # Mostrar taxonomia
    for categoria, keywords in TAXONOMIA.items():
        with st.expander(f"📑 {categoria}"):
            for kw in keywords:
                st.markdown(f"- {kw}")

# Reports Tab
with tabs[2]:
    st.subheader("Reports")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Posts LinkedIn",
            len(linkedin_data),
            "2 novos"
        )
    with col2:
        st.metric(
            "Notícias",
            len(alerts_data),
            "3 novas"
        )
    with col3:
        st.metric(
            "Ações Bomba",
            len(linkedin_data[linkedin_data['classificacao'] == 'Bomba']) + 
            len(alerts_data[alerts_data['classificacao'] == 'Bomba']),
            "1 nova"
        )
    with col4:
        st.metric(
            "Ações Ninja",
            len(linkedin_data[linkedin_data['classificacao'] == 'Ação Ninja']) + 
            len(alerts_data[alerts_data['classificacao'] == 'Ação Ninja']),
            "1 nova"
        )
    
    # Timeline de ações
    st.markdown("### Timeline de Ações")
    
    # Combinar dados de LinkedIn e Google Alerts
    all_actions = pd.concat([
        linkedin_data[['data', 'empresa', 'classificacao', 'relevancia']],
        alerts_data[['data', 'fonte', 'classificacao', 'relevancia']].rename(columns={'fonte': 'empresa'})
    ])
    
    fig_timeline = px.scatter(
        all_actions,
        x='data',
        y='empresa',
        color='classificacao',
        size='relevancia',
        title="Timeline de Ações por Empresa"
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)

# Chat Tab
with tabs[3]:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Sidebar - Configurações e Filtros
with st.sidebar:
    st.header("Configurações")
    
    # Fontes ativas
    st.subheader("Fontes de Dados")
    fontes = {
        "LinkedIn": True,
        "Google Alerts": True,
        "Portal de Notícias": False,
        "Twitter": False
    }
    
    for fonte, status in fontes.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(fonte, value=status)
        with col2:
            if status:
                st.success("✓")
            else:
                st.warning("×")
    
    # Palavras-chave
    st.subheader("Monitoramento")
    with st.expander("📝 Palavras-chave"):
        for categoria in TAXONOMIA.keys():
            st.checkbox(categoria, value=True)
    
    # Configurações de alerta
    st.subheader("Alertas")
    st.checkbox("Notificar ações Bomba", value=True)
    st.checkbox("Notificar ações Ninja", value=True)
    st.checkbox("Resumo diário", value=True)

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
