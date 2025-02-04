import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# [Widget da Zaia permanece igual]

# Funções de análise
def generate_sentiment_data():
    """Gera dados simulados de sentimento para produtos"""
    produtos = ['Hidratante', 'Protetor Solar', 'Sérum', 'Máscara Facial']
    marcas = ['Natura', 'Avon', 'Boticário']
    
    reviews = []
    np.random.seed(42)
    
    for produto in produtos:
        for marca in marcas:
            n_reviews = np.random.randint(50, 200)
            
            # Simula diferentes distribuições de sentimento para cada marca
            if marca == 'Natura':
                sentiments = np.random.normal(0.7, 0.2, n_reviews)
            elif marca == 'Avon':
                sentiments = np.random.normal(0.6, 0.25, n_reviews)
            else:
                sentiments = np.random.normal(0.65, 0.22, n_reviews)
                
            sentiments = np.clip(sentiments, -1, 1)
            
            for sentiment in sentiments:
                reviews.append({
                    'produto': produto,
                    'marca': marca,
                    'sentimento': sentiment,
                    'data': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 30))
                })
    
    return pd.DataFrame(reviews)

def generate_trend_forecast():
    """Gera previsão de tendências simulada"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Tendência base
    trend = np.linspace(0, 2, len(dates))
    
    # Sazonalidade
    seasonality = np.sin(np.linspace(0, 4*np.pi, len(dates))) * 0.3
    
    # Ruído
    noise = np.random.normal(0, 0.1, len(dates))
    
    # Combina componentes
    signal = trend + seasonality + noise
    
    # Normaliza para valores realistas
    scaler = MinMaxScaler(feature_range=(30, 100))
    signal_scaled = scaler.fit_transform(signal.reshape(-1, 1)).flatten()
    
    return pd.DataFrame({
        'data': dates,
        'valor': signal_scaled,
        'tipo': 'histórico'
    })

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

# Carrega dados
sentiment_data = generate_sentiment_data()
forecast_data = generate_trend_forecast()
segment_data = generate_market_segments()

# Header
st.title("🎯 Plataforma IC Natura")

# Main Content
tabs = st.tabs(["📊 Tendências de Mercado", "😊 Análise de Sentimento", "🔮 Previsões", "🎯 Segmentação", "💬 Assistente IA"])

# Tab de Tendências de Mercado
with tabs[0]:
    st.subheader("Análise de Tendências de Mercado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Market Share por Segmento
        fig_segments = px.treemap(
            segment_data,
            path=['segmento', 'marca'],
            values='share',
            title='Market Share por Segmento'
        )
        st.plotly_chart(fig_segments, use_container_width=True)
    
    with col2:
        # Performance por Marca
        fig_performance = px.bar(
            segment_data.groupby('marca')['share'].sum().reset_index(),
            x='marca',
            y='share',
            title='Share Total por Marca',
            color='marca'
        )
        st.plotly_chart(fig_performance, use_container_width=True)

# Tab de Análise de Sentimento
with tabs[1]:
    st.subheader("Análise de Sentimento dos Produtos")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        selected_product = st.selectbox('Produto', sentiment_data['produto'].unique())
    with col2:
        selected_brand = st.multiselect('Marca', sentiment_data['marca'].unique(), default=sentiment_data['marca'].unique())
    
    filtered_data = sentiment_data[
        (sentiment_data['produto'] == selected_product) &
        (sentiment_data['marca'].isin(selected_brand))
    ]
    
    # Gráfico de sentimento
    fig_sentiment = px.box(
        filtered_data,
        x='marca',
        y='sentimento',
        color='marca',
        title=f'Distribuição de Sentimento - {selected_product}'
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Métricas de sentimento
    metrics = filtered_data.groupby('marca')['sentimento'].agg(['mean', 'std', 'count']).round(3)
    
    col1, col2, col3 = st.columns(3)
    for idx, (marca, row) in enumerate(metrics.iterrows()):
        with [col1, col2, col3][idx % 3]:
            st.metric(
                f"{marca}",
                f"Score: {row['mean']:.2f}",
                f"Reviews: {row['count']}"
            )

# Tab de Previsões
with tabs[2]:
    st.subheader("Previsão de Tendências")
    
    # Gráfico de previsão
    fig_forecast = go.Figure()
    
    # Dados históricos
    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_data['data'],
            y=forecast_data['valor'],
            name="Tendência",
            line=dict(color="#1f77b4", width=2)
        )
    )
    
    # Intervalo de confiança
    upper = forecast_data['valor'] * 1.1
    lower = forecast_data['valor'] * 0.9
    
    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_data['data'],
            y=upper,
            fill=None,
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
            name="Upper Bound"
        )
    )
    
    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_data['data'],
            y=lower,
            fill="tonexty",
            fillcolor="rgba(0,176,246,0.2)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
            name="Lower Bound"
        )
    )
    
    fig_forecast.update_layout(
        title="Previsão de Tendências para 2024",
        xaxis_title="Data",
        yaxis_title="Índice de Tendência",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Insights de previsão
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🔍 **Insights Principais**\n"
                "- Tendência de crescimento sustentado\n"
                "- Pico esperado em julho/2024\n"
                "- Sazonalidade marcante no segundo semestre")
    
    with col2:
        st.warning("⚠️ **Pontos de Atenção**\n"
                  "- Possível desaceleração em setembro\n"
                  "- Alta volatilidade no último trimestre\n"
                  "- Necessidade de ações preventivas")

# Tab de Segmentação
with tabs[3]:
    st.subheader("Segmentação de Mercado")
    
    # Mapa de calor de correlações
    correlation_matrix = pd.pivot_table(
        segment_data,
        values='share',
        index='segmento',
        columns='marca'
    ).corr()
    
    fig_heatmap = px.imshow(
        correlation_matrix,
        text=correlation_matrix.round(2),
        aspect="auto",
        title="Correlação entre Marcas por Segmento"
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Análise de composição
    col1, col2 = st.columns(2)
    
    with col1:
        fig_composition = px.sunburst(
            segment_data,
            path=['segmento', 'marca'],
            values='share',
            title="Composição do Mercado"
        )
        st.plotly_chart(fig_composition, use_container_width=True)
    
    with col2:
        st.subheader("Insights de Segmentação")
        st.write("""
        **Principais Observações:**
        - Natura lidera em Perfumaria
        - Maior competição em Maquiagem
        - Oportunidade em Skincare
        
        **Recomendações:**
        1. Fortalecer presença em Skincare
        2. Defender posição em Perfumaria
        3. Inovar em Maquiagem
        """)

# Tab do Assistente
with tabs[4]:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Sidebar com fontes permanece igual

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
