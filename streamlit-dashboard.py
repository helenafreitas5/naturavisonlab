import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler
import random
from faker import Faker
import io

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

# Funções de análise (dados já existentes)
def generate_sentiment_data():
    """Gera dados simulados de sentimento para produtos"""
    produtos = ['Hidratante', 'Protetor Solar', 'Sérum', 'Máscara Facial']
    marcas = ['Natura', 'Avon', 'Boticário']
    
    reviews = []
    np.random.seed(42)
    
    for produto in produtos:
        for marca in marcas:
            n_reviews = np.random.randint(50, 200)
            sentiments = np.random.normal(0.7, 0.2, n_reviews)
            sentiments = np.clip(sentiments, -1, 1)
            
            for sentiment in sentiments:
                reviews.append({
                    'produto': produto,
                    'marca': marca,
                    'sentimento': sentiment,
                    'data': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 30))
                })
    
    return pd.DataFrame(reviews)

def generate_market_segments():
    """Gera dados simulados de segmentação de mercado"""
    segments = {
        'Skincare': {
            'Natura': 35,
            'Avon': 25,
            'Boticário': 20,
            'Outros': 20
        },
        'Maquiagem': {
            'Natura': 30,
            'Avon': 28,
            'Boticário': 25,
            'Outros': 17
        },
        'Perfumaria': {
            'Natura': 40,
            'Avon': 20,
            'Boticário': 25,
            'Outros': 15
        }
    }
    
    data = []
    for segment, shares in segments.items():
        for brand, share in shares.items():
            data.append({
                'segmento': segment,
                'marca': brand,
                'share': share
            })
    
    return pd.DataFrame(data)

# Novas funções para gerar dados fictícios de tendências de mercado externas
def generate_trends_market_data(num_records=100):
    fake = Faker('pt_BR')
    data_inicio = datetime.today() - timedelta(days=365)
    data_fim = datetime.today()
    categorias = ["Perfumaria", "Cosméticos", "Maquiagem", "Skin Care"]
    fontes = ["Google Trends", "Redes Sociais", "Pesquisas de Mercado", "Consultoria Externa"]
    tendencias = ["Crescente", "Estável", "Decrescente"]
    lista = []
    for _ in range(num_records):
         random_date = data_inicio + timedelta(days=random.randint(0, (data_fim - data_inicio).days))
         registro = {
              'Data': random_date.date(),
              'Categoria': random.choice(categorias),
              'Tendência': random.choice(tendencias),
              'Índice': round(random.uniform(0, 100), 2),
              'Fonte': random.choice(fontes),
              'Observações': fake.sentence(nb_words=10)
         }
         lista.append(registro)
    return pd.DataFrame(lista)

def generate_external_sentiment_data(num_records=50):
    data_inicio = datetime.today() - timedelta(days=365)
    data_fim = datetime.today()
    categorias = ["Perfumaria", "Cosméticos", "Maquiagem", "Skin Care"]
    plataformas = ["Twitter", "Instagram", "Facebook", "YouTube", "Blogs"]
    sentimentos = ["Positivo", "Neutro", "Negativo"]
    lista = []
    for _ in range(num_records):
         random_date = data_inicio + timedelta(days=random.randint(0, (data_fim - data_inicio).days))
         registro = {
              'Data': random_date.date(),
              'Categoria': random.choice(categorias),
              'Plataforma': random.choice(plataformas),
              'Sentimento': random.choice(sentimentos),
              'Volume': random.randint(100, 10000)
         }
         lista.append(registro)
    return pd.DataFrame(lista)

# Carrega dados existentes
sentiment_data = generate_sentiment_data()
segment_data = generate_market_segments()

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

# Main Content - agora com 4 abas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💬 Assistente IA", "📈 Análise", "🌐 Tendências Externas"])

# Dashboard Tab
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Análise de Sentimento")
        # Gráfico de sentimento por marca
        fig_sentiment = px.box(
            sentiment_data,
            x='marca',
            y='sentimento',
            color='marca',
            title='Sentimento por Marca'
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
        
        st.subheader("Market Share")
        fig_market = px.treemap(
            segment_data,
            path=['segmento', 'marca'],
            values='share',
            title='Participação de Mercado por Segmento'
        )
        st.plotly_chart(fig_market, use_container_width=True)
    
    with col2:
        st.subheader("Correlação entre Marcas")
        # Mapa de calor de correlações
        correlation_matrix = pd.pivot_table(
            segment_data,
            values='share',
            index='segmento',
            columns='marca'
        ).corr()
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            text=correlation_matrix.round(2),
            texttemplate='%{text}',
            textfont={"size": 12},
            hoverongaps=False,
            colorscale='RdBu'
        ))
        
        fig_heatmap.update_layout(
            title="Correlação entre Marcas por Segmento",
            xaxis_title="Marca",
            yaxis_title="Marca",
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.subheader("Performance por Segmento")
        fig_performance = px.bar(
            segment_data.groupby('segmento')['share'].sum().reset_index(),
            x='segmento',
            y='share',
            title='Share Total por Segmento',
            color='segmento'
        )
        st.plotly_chart(fig_performance, use_container_width=True)

# Chat Tab com widget da Zaia
with tab2:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Análise Tab
with tab3:
    st.subheader("Studio")
    
    # Quick Dashboard
    st.markdown("#### 🎯 Dashboard Rápido")
    dash_container = st.container()
    with dash_container:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Análise de Mercado"):
                st.metric("Market Share", "35%", "2.5%")
                
        with col2:
            if st.button("💭 Análise de Sentimento"):
                st.metric("Sentimento Médio", "0.72", "0.05")
                
        with col3:
            if st.button("📈 Previsões"):
                st.metric("Tendência", "Crescente", "15%")
    
    # Report Generation
    st.markdown("#### 📑 Relatórios")
    with st.expander("📊 Análise de Performance"):
        st.write("Análise de performance do último trimestre:")
        st.write("• Market share cresceu 2.5% vs trimestre anterior")
        st.write("• Sentimento positivo em 72% das menções")
        st.write("• Liderança em 2 de 3 segmentos principais")
    
    with st.expander("💡 Recomendações"):
        st.write("• Investir em segmentos com maior potencial")
        st.write("• Monitorar ações da concorrência")
        st.write("• Fortalecer presença digital")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Exportar Relatório"):
            st.success("Relatório exportado com sucesso!")
    with col2:
        if st.button("📧 Compartilhar"):
            st.success("Link de compartilhamento gerado!")

# Tendências Externas Tab - novos dados fictícios
with tab4:
    st.subheader("Dados de Tendências de Mercado Externas")
    trends_df = generate_trends_market_data()
    sentiment_ext_df = generate_external_sentiment_data()
    
    st.markdown("##### Tendências de Mercado")
    st.dataframe(trends_df)
    
    st.markdown("##### Análise de Sentimento Externa")
    st.dataframe(sentiment_ext_df)
    
    # Opção para download das planilhas em Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
         trends_df.to_excel(writer, sheet_name="Tendências_Mercado", index=False)
         sentiment_ext_df.to_excel(writer, sheet_name="Análise_Sentimento", index=False)
    output.seek(0)
    st.download_button(
         label="Download Planilhas Fictícias",
         data=output,
         file_name="demo_MVP_tendencias_Natura.xlsx",
         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

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
