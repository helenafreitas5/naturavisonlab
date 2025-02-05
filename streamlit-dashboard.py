import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Configurações e dados simulados
COMPETITORS = ["O Boticário", "Avon", "Eudora", "MAC", "Quem disse Berenice"]
TERRITORIES = ["Digital", "Sustentabilidade", "Experiência", "Inovação"]
CATEGORIES = ["Skincare", "Makeup", "Perfumes", "Corpo", "Rosto"]

# Função para dados simulados
def generate_mock_data():
    """Gera dados simulados para a plataforma"""
    # Movimentos competitivos
    movements = pd.DataFrame({
        'data': pd.date_range(start='2024-01-01', end='2024-02-04', freq='D'),
        'empresa': np.random.choice(COMPETITORS, 35),
        'territorio': np.random.choice(TERRITORIES, 35),
        'categoria': np.random.choice(CATEGORIES, 35),
        'relevancia': np.random.randint(1, 6, 35),
        'tipo': np.random.choice(['BAU', 'Bomba', 'Ninja'], 35, p=[0.7, 0.2, 0.1])
    })
    
    # Engajamento
    movements['engajamento'] = np.random.randint(100, 10000, 35)
    
    # Descrições simuladas
    acoes = [
        "Lançamento de nova linha",
        "Campanha nas redes sociais",
        "Parceria com influenciador",
        "Expansão de mercado",
        "Programa de fidelidade",
        "Inovação em produto",
        "Ação sustentável"
    ]
    movements['descricao'] = np.random.choice(acoes, 35)
    
    return movements

# Widget do Agente ZAIA
def zaia_widget():
    """Widget do Agente ZAIA"""
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

# Carrega dados simulados
movements_data = generate_mock_data()

# Interface principal
st.title("🎯 Plataforma IC Natura")

# Main Content
tabs = st.tabs(["📊 Dashboard", "🔍 Fonte de Dados", "💬 Assistente IA", "📈 Studio"])

# Dashboard Tab
with tabs[0]:
    st.subheader("Overview de Mercado")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Movimentos", len(movements_data), "+3")
    with col2:
        st.metric("Ações Bomba", len(movements_data[movements_data['tipo'] == 'Bomba']), "+1")
    with col3:
        st.metric("Relevância Média", f"{movements_data['relevancia'].mean():.1f}", "+0.2")
    with col4:
        st.metric("Engajamento Total", f"{movements_data['engajamento'].sum():,}", "+12%")

    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        # Movimentos por território
        fig = px.bar(
            movements_data['territorio'].value_counts().reset_index(),
            x='territorio',
            y='count',
            title="Movimentos por Território"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribuição de tipos
        fig = px.pie(
            movements_data['tipo'].value_counts().reset_index(),
            values='count',
            names='tipo',
            title="Distribuição por Tipo de Ação"
        )
        st.plotly_chart(fig, use_container_width=True)

# Fonte de Dados Tab
with tabs[1]:
    st.subheader("Fontes de Dados")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_competitor = st.multiselect(
            "Empresas",
            COMPETITORS,
            default=COMPETITORS[:2]
        )
    with col2:
        selected_territory = st.multiselect(
            "Territórios",
            TERRITORIES,
            default=TERRITORIES[:2]
        )
    with col3:
        date_range = st.date_input(
            "Período",
            [datetime.now() - timedelta(days=30), datetime.now()]
        )
    
    # Timeline de movimentos
    st.markdown("### Timeline de Movimentos")
    
    filtered_data = movements_data[
        (movements_data['empresa'].isin(selected_competitor)) &
        (movements_data['territorio'].isin(selected_territory))
    ]
    
    for _, movement in filtered_data.iterrows():
        with st.expander(f"{movement['data'].strftime('%d/%m/%Y')} - {movement['empresa']}: {movement['descricao']}"):
            col1, col2 = st.columns([3,1])
            
            with col1:
                st.markdown(f"**Território:** {movement['territorio']}")
                st.markdown(f"**Categoria:** {movement['categoria']}")
                st.markdown(f"**Engajamento:** {movement['engajamento']:,}")
            
            with col2:
                if movement['tipo'] == 'Bomba':
                    st.error(movement['tipo'])
                elif movement['tipo'] == 'Ninja':
                    st.warning(movement['tipo'])
                else:
                    st.info(movement['tipo'])
                st.metric("Relevância", movement['relevancia'])

# Assistente IA Tab
with tabs[2]:
    st.subheader("💬 Assistente Natura")
    zaia_widget()

# Studio Tab
with tabs[3]:
    st.subheader("Data Studio")
    
    # Seleção de análise
    analysis_type = st.selectbox(
        "Tipo de Análise",
        ["Quick Analysis", "Competitive Report", "Territory Deep Dive"]
    )
    
    if analysis_type == "Quick Analysis":
        # Análise rápida
        col1, col2 = st.columns(2)
        
        with col1:
            # Timeline
            fig = px.scatter(
                movements_data,
                x='data',
                y='empresa',
                size='relevancia',
                color='tipo',
                title="Timeline de Ações"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Heatmap de territórios
            territory_matrix = pd.crosstab(movements_data['empresa'], movements_data['territorio'])
            fig = px.imshow(
                territory_matrix,
                title="Heatmap de Territórios"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Competitive Report":
        # Relatório competitivo
        st.markdown("### Análise Competitiva")
        
        # Métricas por empresa
        for competitor in COMPETITORS[:3]:
            comp_data = movements_data[movements_data['empresa'] == competitor]
            
            st.markdown(f"#### {competitor}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Ações", len(comp_data))
            with col2:
                st.metric("Relevância Média", f"{comp_data['relevancia'].mean():.1f}")
            with col3:
                st.metric("% Ações Relevantes", f"{(len(comp_data[comp_data['relevancia'] >= 4]) / len(comp_data) * 100):.1f}%")
    
    else:  # Territory Deep Dive
        # Análise de território
        selected_territory = st.selectbox(
            "Território",
            TERRITORIES
        )
        
        territory_data = movements_data[movements_data['territorio'] == selected_territory]
        
        # Análise do território
        col1, col2 = st.columns(2)
        
        with col1:
            # Ações por empresa no território
            fig = px.bar(
                territory_data['empresa'].value_counts().reset_index(),
                x='empresa',
                y='count',
                title=f"Ações em {selected_territory}"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Relevância média por empresa
            fig = px.bar(
                territory_data.groupby('empresa')['relevancia'].mean().reset_index(),
                x='empresa',
                y='relevancia',
                title=f"Relevância Média em {selected_territory}"
            )
            st.plotly_chart(fig, use_container_width=True)

# Sidebar
with st.sidebar:
    st.header("Configurações")
    
    # Fontes ativas
    st.subheader("Fontes de Dados")
    sources = {
        "Google Trends": True,
        "LinkedIn": True,
        "Notícias": True,
        "Redes Sociais": False
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
    
    # Configurações de alerta
    st.subheader("Alertas")
    st.checkbox("Alertas de Bomba", value=True)
    st.checkbox("Alertas de Ninja", value=True)
    alert_relevance = st.slider(
        "Relevância mínima",
        1, 5, 4
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
