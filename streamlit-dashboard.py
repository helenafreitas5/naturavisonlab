import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import numpy as np
from collections import defaultdict
import re
from textblob import TextBlob

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Configurações e constantes
COMPETITORS = ["O Boticário", "Avon", "Eudora", "MAC", "Quem disse Berenice"]

# Configuração da rede semântica
SEMANTIC_NETWORK = {
    'Inovação': {
        'primary': ['tecnologia', 'inovação', 'digital', 'futuro'],
        'related': ['desenvolvimento', 'pesquisa', 'lançamento'],
        'weight': 1.0
    },
    'Sustentabilidade': {
        'primary': ['sustentável', 'eco', 'verde', 'ambiental'],
        'related': ['reciclável', 'natural', 'consciente'],
        'weight': 0.8
    },
    'Experiência': {
        'primary': ['cliente', 'experiência', 'jornada', 'atendimento'],
        'related': ['personalização', 'serviço', 'satisfação'],
        'weight': 0.9
    },
    'Produto': {
        'primary': ['skincare', 'maquiagem', 'perfume', 'tratamento'],
        'related': ['fórmula', 'ingredientes', 'linha'],
        'weight': 0.7
    }
}

# Classificação de ações
ACTION_TYPES = {
    'BAU': {
        'keywords': ['regular', 'rotina', 'normal', 'padrão'],
        'weight': 0.3,
        'threshold': 0.4
    },
    'Bomba': {
        'keywords': ['inovador', 'disruptivo', 'revolucionário', 'único'],
        'weight': 0.8,
        'threshold': 0.7
    },
    'Ninja': {
        'keywords': ['estratégico', 'silencioso', 'surpresa', 'inesperado'],
        'weight': 0.6,
        'threshold': 0.6
    }
}

# Classes e funções principais
class SemanticAnalyzer:
    def __init__(self, semantic_network, action_types):
        self.semantic_network = semantic_network
        self.action_types = action_types
        
    def analyze_text(self, text):
        """Analisa texto e retorna classificações e territórios"""
        text = text.lower()
        blob = TextBlob(text)
        
        # Análise de territórios
        territory_scores = defaultdict(float)
        for territory, data in self.semantic_network.items():
            primary_score = sum(word in text for word in data['primary']) * data['weight']
            related_score = sum(word in text for word in data['related']) * data['weight'] * 0.7
            territory_scores[territory] = primary_score + related_score
        
        # Análise de tipo de ação
        action_scores = defaultdict(float)
        for action, data in self.action_types.items():
            score = sum(word in text for word in data['keywords']) * data['weight']
            if score >= data['threshold']:
                action_scores[action] = score
        
        # Identifica principais territórios e ação
        main_territories = [t for t, s in territory_scores.items() if s > 0.5]
        main_action = max(action_scores.items(), key=lambda x: x[1])[0] if action_scores else 'BAU'
        
        return {
            'territories': main_territories,
            'action_type': main_action,
            'sentiment': blob.sentiment.polarity,
            'relevance': max(action_scores.values()) if action_scores else 0.3
        }

def generate_mock_data():
    """Gera dados simulados enriquecidos"""
    # Ações base
    actions = [
        "Lançamento de nova linha de skincare sustentável com tecnologia coreana",
        "Campanha digital com 50 influenciadores para linha de maquiagem",
        "Expansão de lojas no Nordeste com novo conceito de experiência",
        "Parceria internacional com marca francesa de luxo",
        "Novo app de realidade aumentada para teste de produtos",
        "Programa de reciclagem de embalagens em parceria com cooperativas",
        "Sistema de refil para toda linha de perfumes premium",
        "Loja conceito com tecnologia de personalização",
        "Nova linha de tratamento anti-idade com ativos da biodiversidade",
        "Marketplace próprio com sistema de consultoria online"
    ]
    
    # Cria DataFrame
    data = []
    analyzer = SemanticAnalyzer(SEMANTIC_NETWORK, ACTION_TYPES)
    
    # Gera dados para os últimos 35 dias
    start_date = pd.Timestamp.now() - pd.Timedelta(days=35)
    
    for _ in range(35):
        action = np.random.choice(actions)
        analysis = analyzer.analyze_text(action)
        
        data.append({
            'data': start_date + pd.Timedelta(days=np.random.randint(0, 35)),
            'empresa': np.random.choice(COMPETITORS),
            'acao': action,
            'territorios': analysis['territories'],
            'tipo': analysis['action_type'],
            'relevancia': max(1, min(5, int(analysis['relevance'] * 5))),
            'sentimento': analysis['sentiment'],
            'engajamento': np.random.randint(100, 10000)
        })
    
    return pd.DataFrame(data)

def generate_network(data):
    """Gera rede de conexões entre empresas e territórios"""
    G = nx.Graph()
    
    # Adiciona nós
    for territory in SEMANTIC_NETWORK.keys():
        G.add_node(territory, type='territory')
    
    for competitor in COMPETITORS:
        G.add_node(competitor, type='competitor')
    
    # Adiciona conexões baseadas em ações
    for _, row in data.iterrows():
        for territory in row['territorios']:
            # Peso da conexão baseado na relevância
            weight = row['relevancia'] / 5.0
            
            # Adiciona ou atualiza conexão
            if G.has_edge(row['empresa'], territory):
                G[row['empresa']][territory]['weight'] += weight
            else:
                G.add_edge(row['empresa'], territory, weight=weight)
    
    return G

# Widget do Agente ZAIA
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

# Função para análise de tendências
def analyze_trends(data, window_size=7):
    """Analisa tendências nos dados"""
    # Agregar dados por território e data
    territory_trends = pd.DataFrame([
        {'data': row['data'], 'territorio': t, 'relevancia': row['relevancia']}
        for _, row in data.iterrows()
        for t in row['territorios']
    ])
    
    # Calcular médias móveis
    trends = {}
    for territory in SEMANTIC_NETWORK.keys():
        territory_data = territory_trends[territory_trends['territorio'] == territory]
        if not territory_data.empty:
            trends[territory] = {
                'mean': territory_data['relevancia'].mean(),
                'trend': territory_data['relevancia'].diff().mean(),
                'volume': len(territory_data)
            }
    
    return trends

# Carrega dados simulados
movements_data = generate_mock_data()

# Interface principal
st.title("🎯 Plataforma IC Natura")

# Main Content
tabs = st.tabs(["📊 Dashboard", "🔍 Fonte de Dados", "🕸️ Análise Semântica", "💬 Assistente IA", "📈 Studio"])

# Dashboard Tab
with tabs[0]:
    st.subheader("Overview de Mercado")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Movimentos",
            len(movements_data),
            f"+{len(movements_data[movements_data['data'] > pd.Timestamp.now() - pd.Timedelta(days=7)])}"
        )
    
    with col2:
        bomba_count = len(movements_data[movements_data['tipo'] == 'Bomba'])
        st.metric(
            "Ações Bomba",
            bomba_count,
            f"+{len(movements_data[(movements_data['tipo'] == 'Bomba') & (movements_data['data'] > pd.Timestamp.now() - pd.Timedelta(days=7))])}"
        )
    
    with col3:
        avg_relevance = movements_data['relevancia'].mean()
        st.metric(
            "Relevância Média",
            f"{avg_relevance:.1f}",
            f"{(avg_relevance - 3):.1f}"
        )
    
    with col4:
        total_engagement = movements_data['engajamento'].sum()
        st.metric(
            "Engajamento Total",
            f"{total_engagement:,.0f}",
            "12%"
        )
    
    # Visualizações principais
    col1, col2 = st.columns(2)
    
    with col1:
        # Timeline de ações
        fig = px.scatter(
            movements_data,
            x='data',
            y='empresa',
            size='relevancia',
            color='tipo',
            title="Timeline de Ações",
            height=400
        )
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Empresa",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Heatmap de territórios por empresa
        territory_data = pd.DataFrame([
            {'empresa': row['empresa'], 'territorio': t}
            for _, row in movements_data.iterrows()
            for t in row['territorios']
        ])
        
        territory_matrix = pd.crosstab(territory_data['empresa'], territory_data['territorio'])
        
        fig = px.imshow(
            territory_matrix,
            title="Intensidade de Atuação por Território",
            height=400,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de tendências
    st.subheader("Tendências e Insights")
    
    # Análise de tendências por território
    trends = analyze_trends(movements_data)
    
    # Exibir insights baseados nas tendências
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Territórios em Alta")
        for territory, data in trends.items():
            if data['trend'] > 0:
                st.markdown(f"""
                **{territory}**
                - Volume: {data['volume']} ações
                - Tendência: ↗️ +{abs(data['trend']):.2f}
                """)
    
    with col2:
        st.markdown("#### 📉 Territórios em Observação")
        for territory, data in trends.items():
            if data['trend'] < 0:
                st.markdown(f"""
                **{territory}**
                - Volume: {data['volume']} ações
                - Tendência: ↘️ {data['trend']:.2f}
                """)

# Fonte de Dados Tab
with tabs[1]:
    st.subheader("Fonte de Dados")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_companies = st.multiselect(
            "Empresas",
            COMPETITORS,
            default=COMPETITORS[:2]
        )
    
    with col2:
        selected_territories = st.multiselect(
            "Territórios",
            list(SEMANTIC_NETWORK.keys()),
            default=list(SEMANTIC_NETWORK.keys())[:2]
        )
    
    with col3:
        selected_types = st.multiselect(
            "Tipos de Ação",
            list(ACTION_TYPES.keys()),
            default=['Bomba', 'Ninja']
        )
    
    # Dados filtrados
    filtered_data = movements_data[
        (movements_data['empresa'].isin(selected_companies)) &
        (movements_data['tipo'].isin(selected_types))
    ]
    
    # Lista de movimentos
    st.markdown("### Movimentos Identificados")
    
    for _, movement in filtered_data.iterrows():
        with st.expander(f"{movement['data'].strftime('%d/%m/%Y')} - {movement['empresa']}: {movement['acao']}"):
            col1, col2 = st.columns([3,1])
            
            with col1:
                st.markdown(f"**Territórios:** {', '.join(movement['territorios'])}")
                st.markdown(f"**Sentimento:** {'Positivo' if movement['sentimento'] > 0 else 'Negativo'} ({movement['sentimento']:.2f})")
                st.markdown(f"**Engajamento:** {movement['engajamento']:,}")
            
            with col2:
                if movement['tipo'] == 'Bomba':
                    st.error(movement['tipo'])
                elif movement['tipo'] == 'Ninja':
                    st.warning(movement['tipo'])
                else:
                    st.info(movement['tipo'])
                st.metric("Relevância", movement['relevancia'])

# Análise Semântica Tab
with tabs[2]:
    st.subheader("Análise Semântica de Mercado")
    
    # Rede de conexões
    st.markdown("### Rede de Conexões")
    network = generate_network(movements_data)
    
    # Criar visualização de rede usando Plotly
    pos = nx.spring_layout(network)
    
    edge_x = []
    edge_y = []
    for edge in network.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    for
