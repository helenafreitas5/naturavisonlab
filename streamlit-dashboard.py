import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from pytrends.request import TrendReq

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Configuração das fontes de dados
@st.cache_data(ttl=3600)
def get_google_trends_data():
    try:
        pytrends = TrendReq(hl='pt-BR')
        
        # Lista de palavras-chave relevantes para o negócio
        keywords_groups = {
            'Tipos de Pele': ["pele oleosa", "pele seca", "pele mista", "pele sensível"],
            'Categorias': ["skincare", "maquiagem", "perfume", "cosméticos naturais"],
            'Tratamentos': ["anti-idade", "acne", "hidratação", "protetor solar"]
        }
        
        all_data = {}
        for category, keywords in keywords_groups.items():
            pytrends.build_payload(keywords, timeframe='today 12-m', geo='BR')
            data = pytrends.interest_over_time()
            if 'isPartial' in data.columns:
                data = data.drop('isPartial', axis=1)
            all_data[category] = data
            
        # Buscar dados geográficos para principais termos
        pytrends.build_payload(["natura cosméticos"], timeframe='today 12-m', geo='BR')
        geo_data = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
        
        return all_data, geo_data
    except Exception as e:
        st.error(f"Erro ao buscar dados do Google Trends: {str(e)}")
        return None, None

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
trends_data, geo_data = get_google_trends_data()

# Header
st.title("🎯 Plataforma IC Natura")

# Sidebar - Fontes de Dados
with st.sidebar:
    st.header("Fontes de Dados")
    
    # Status das fontes
    st.subheader("Status das Fontes")
    sources = {
        "Google Trends": trends_data is not None,
        "Social Media": False,
        "E-commerce": False,
        "CRM": False
    }
    
    for source, active in sources.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(source)
        with col2:
            if active:
                st.success("✓")
            else:
                st.warning("×")
    
    # Filtros
    st.subheader("Filtros")
    if trends_data:
        selected_category = st.selectbox(
            "Categoria de Análise",
            list(trends_data.keys())
        )
        
        time_range = st.select_slider(
            "Período de Análise",
            options=["1 Mês", "3 Meses", "6 Meses", "12 Meses"],
            value="3 Meses"
        )

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Assistente IA", "📈 Análise Detalhada"])

# Dashboard Tab
with tab1:
    if trends_data:
        st.subheader("Insights do Mercado")
        
        # Métricas principais
        cols = st.columns(4)
        current_data = trends_data[selected_category]
        for idx, keyword in enumerate(current_data.columns):
            with cols[idx]:
                current_value = current_data[keyword].iloc[-1]
                previous_value = current_data[keyword].iloc[-2]
                delta = current_value - previous_value
                st.metric(
                    label=keyword,
                    value=f"{current_value:.0f}",
                    delta=f"{delta:.1f}%"
                )
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            # Tendências ao longo do tempo
            st.subheader("Tendências de Busca")
            fig = px.line(current_data)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if geo_data is not None:
                # Mapa de calor por região
                st.subheader("Interesse por Região")
                fig = px.choropleth(
                    geo_data,
                    locations=geo_data.index,
                    locationmode="country names",
                    color=geo_data.columns[0],
                    scope="south america",
                    center={"lat": -14.2350, "lon": -51.9253}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Análise de tendências
        st.subheader("Análise Comparativa")
        selected_data = current_data.copy()
        selected_data['month'] = selected_data.index.month
        monthly_avg = selected_data.groupby('month').mean()
        
        fig = px.line(monthly_avg, title="Sazonalidade por Termo")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("Não foi possível carregar os dados do Google Trends")

# Chat Tab
with tab2:
    st.subheader("💬 Chat com Assistente Natura")
    zaia_widget()

# Análise Detalhada Tab
with tab3:
    if trends_data:
        st.subheader("Análise Detalhada de Tendências")
        
        # Análise de correlação
        st.subheader("Correlação entre Termos")
        corr_matrix = current_data.corr()
        fig = px.imshow(
            corr_matrix,
            labels=dict(color="Correlação"),
            color_continuous_scale="RdBu"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights automáticos
        st.subheader("Insights Automáticos")
        
        # Identificar tendências crescentes/decrescentes
        for keyword in current_data.columns:
            trend = current_data[keyword].iloc[-30:].mean() - current_data[keyword].iloc[-60:-30].mean()
            if abs(trend) > 5:
                direction = "crescimento" if trend > 0 else "queda"
                st.info(f"📈 {keyword}: {direction} de {abs(trend):.1f}% nos últimos 30 dias")
        
        # Top correlações
        st.subheader("Principais Correlações")
        correlations = corr_matrix.unstack()
        correlations = correlations[correlations != 1.0].sort_values(ascending=False)
        st.write("Termos mais correlacionados:")
        for idx, corr in correlations[:3].items():
            st.write(f"• {idx[0]} × {idx[1]}: {corr:.2f}")

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
