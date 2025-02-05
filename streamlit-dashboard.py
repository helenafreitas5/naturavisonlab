import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime
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
        "Lançamento de nova linha de skincare sustentável",
        "Campanha digital com influenciadores",
        "Expansão de lojas no Nordeste",
        "Parceria com marca internacional",
        "Novo app de realidade aumentada",
        "Programa de reciclagem de embalagens",
        "Sistema de refil para perfumes"
    ]
    
    # Cria DataFrame
    data = []
    analyzer = SemanticAnalyzer(SEMANTIC_NETWORK, ACTION_TYPES)
    
    for _ in range(35):
        action = np.random.choice(actions)
        analysis = analyzer.analyze_text(action)
        
        data.append({
            'data': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 35)),
            'empresa': np.random.choice(COMPETITORS),
            'acao': action,
            'territorios': analysis['territories'],
            'tipo': analysis['action_type'],
            'relevancia': max(1, min(5, int(analysis['relevance'] * 5))),
            'sentimento': analysis['sentiment'],
            'engajamento': np.random.randint(100, 10000)
        })
    
    return pd.DataFrame(data)

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

# Gera rede de conexões
def generate_network(data):
    G = nx.Graph()
    
    # Adiciona nós
    for territory in SEMANTIC_NETWORK.keys():
        G.add_node(territory, type='territory')
    
    for competitor in COMPETITORS:
        G.add_node(competitor, type='competitor')
    
    # Adiciona conexões baseadas em ações
    for _, row in data.iterrows():
        for territory in row['territorios']:
            G.add_edge(row['empresa'], territory, weight=row['relevancia'])
    
    return G

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
            title="Timeline de Ações"
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
            title="Intensidade de Atuação por Território"
        )
        st.plotly_chart(fig, use_container_width=True)

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
                st.markdown(f"**Sentimento:** {movement['sentimento']:.2f}")
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
    for node in network.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if network.nodes[node]['type'] == 'territory':
            node_color.append('red')
        else:
            node_color.append('blue')

    # Criar figura
    fig = go.Figure()
    
    # Adicionar arestas
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Adicionar nós
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=20,
            color=node_color,
            line_width=2
        )
    ))
    
    fig.update_layout(
        title="Rede de Conexões entre Empresas e Territórios",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0,l=0,r=0,t=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de clusters
    st.markdown("### Clusters Temáticos")
    
    # Criar matriz de co-ocorrência
    territories = list(SEMANTIC_NETWORK.keys())
    co_occurrence = np.zeros((len(territories), len(territories)))
    
    for _, row in movements_data.iterrows():
        for t1 in row['territorios']:
            for t2 in row['territorios']:
                if t1 != t2:
                    i = territories.index(t1)
                    j = territories.index(t2)
                    co_occurrence[i][j] += 1
                    co_occurrence[j][i] += 1
    
    fig = px.imshow(
        co_occurrence,
        x=territories,
        y=territories,
        title="Matriz de Co-ocorrência de Territórios"
    )
    st.plotly_chart(fig, use_container_width=True)

# Assistente IA Tab
with tabs[3]:
    st.subheader("💬 Assistente Natura")
    zaia_widget()

# Studio Tab
with tabs[4]:
    st.subheader("Data Studio")
    
    analysis_type = st.selectbox(
        "Tipo de Análise",
        ["Análise Competitiva", "Território Deep Dive", "Tendências Emergentes"]
    )
    
    if analysis_type == "Análise Competitiva":
        st.markdown("### Análise Competitiva")
        
        # Métricas por empresa
        for competitor in selected_companies:
            comp_data = movements_data[movements_data['empresa'] == competitor]
            
            st.markdown(f"#### {competitor}")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Ações", len(comp_data))
            with col2:
                st.metric("Relevância Média", f"{comp_data['relevancia'].mean():.1f}")
            with col3:
                st.metric("Engajamento Total", f"{comp_data['engajamento'].sum():,}")
            
            # Gráfico de ações por território
            territory_counts = pd.DataFrame([
                {'territorio': t}
                for _, row in comp_data.iterrows()
                for t in row['territorios']
            ])
            
            if not territory_counts.empty:
                fig = px.bar(
                    territory_counts['territorio'].value_counts().reset_index(),
                    x='index',
                    y='territorio',
                    title=f"Ações por Território - {competitor}"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Território Deep Dive":
        st.markdown("### Análise de Território")
        
        selected_territory = st.selectbox(
            "Selecione o Território",
            list(SEMANTIC_NETWORK.keys())
        )
        
        # Filtrar ações do território
        territory_actions = movements_data[movements_data['territorios'].apply(lambda x: selected_territory in x)]
        
        # Métricas do território
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Ações", len(territory_actions))
        with col2:
            st.metric("Relevância Média", f"{territory_actions['relevancia'].mean():.1f}")
        with col3:
            st.metric("Engajamento Total", f"{territory_actions['engajamento'].sum():,}")
        
        # Timeline do território
        fig = px.scatter(
            territory_actions,
            x='data',
            y='empresa',
            size='relevancia',
            color='tipo',
            title=f"Timeline de Ações - {selected_territory}"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise de palavras-chave
        st.markdown("#### Palavras-chave Relacionadas")
        st.write(f"Primárias: {', '.join(SEMANTIC_NETWORK[selected_territory]['primary'])}")
        st.write(f"Relacionadas: {', '.join(SEMANTIC_NETWORK[selected_territory]['related'])}")
    
    else:  # Tendências Emergentes
        st.markdown("### Tendências Emergentes")
        
        # Análise temporal de territórios
        territory_trends = pd.DataFrame([
            {'data': row['data'], 'territorio': t, 'relevancia': row['relevancia']}
            for _, row in movements_data.iterrows()
            for t in row['territorios']
        ])
        
        # Agregar por semana
        territory_trends['semana'] = territory_trends['data'].dt.isocalendar().week
        weekly_trends = territory_trends.groupby(['semana', 'territorio'])['relevancia'].mean().reset_index()
        
        fig = px.line(
            weekly_trends,
            x='semana',
            y='relevancia',
            color='territorio',
            title="Evolução de Relevância por Território"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Identificar tendências emergentes
        st.markdown("#### Tendências Identificadas")
        
        last_week = territory_trends['semana'].max()
        previous_week = last_week - 1
        
        for territory in SEMANTIC_NETWORK.keys():
            last_week_data = weekly_trends[
                (weekly_trends['semana'] == last_week) &
                (weekly_trends['territorio'] == territory)
            ]
            previous_week_data = weekly_trends[
                (weekly_trends['semana'] == previous
