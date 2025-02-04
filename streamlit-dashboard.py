import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
import json

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma IC Natura")

# Função para interagir com a Zaia via Webhook
def get_zaia_response(prompt):
    url = "https://api.zaia.app/v1/webhook/agent-incoming-webhook-event/create"
    
    params = {
        "agentIncomingWebhookId": "2469",
        "key": "b58b7e25-5022-4d36-930a-a6c953b8a70b"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": prompt,
        "sessionId": "streamlit-dashboard",
        "source": "dashboard"
    }
    
    try:
        response = requests.post(url, params=params, headers=headers, json=payload)
        st.write(f"Debug - Status: {response.status_code}")  # Debug info
        st.write(f"Debug - Response: {response.text}")  # Debug info
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('message', 'Sem resposta do agente')
        else:
            st.error(f"Erro na API: {response.status_code}")
            return "Desculpe, estou tendo problemas para me comunicar com o servidor. Por favor, tente novamente."
    except Exception as e:
        st.error(f"Erro ao conectar: {str(e)}")
        return "Desculpe, ocorreu um erro na comunicação. Por favor, tente novamente em alguns instantes."

# Inicialização da sessão para o chat
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Olá! Sou o assistente da Natura. Como posso ajudar você hoje?"
    })

# Dados mockados
@st.cache_data
def load_mock_data():
    benchmark_data = pd.DataFrame([
        {"category": "Skincare", "natura": 85, "avon": 75, "boticario": 80},
        {"category": "Makeup", "natura": 78, "avon": 82, "boticario": 85},
        {"category": "Perfumes", "natura": 90, "avon": 85, "boticario": 88}
    ])
    
    trends_data = pd.DataFrame([
        {"month": "Jan", "skincare": 65, "makeup": 45},
        {"month": "Feb", "skincare": 70, "makeup": 52},
        {"month": "Mar", "skincare": 85, "makeup": 58}
    ])
    
    market_data = pd.DataFrame([
        {"name": "Natura", "value": 35},
        {"name": "Avon", "value": 25},
        {"name": "Boticário", "value": 20}
    ])
    
    performance_data = pd.DataFrame([
        {"category": "Skincare", "atual": 92, "meta": 85},
        {"category": "Makeup", "atual": 78, "meta": 80}
    ])
    
    return benchmark_data, trends_data, market_data, performance_data

# Carrega dados
benchmark_data, trends_data, market_data, performance_data = load_mock_data()

# Header
col1, col2, col3 = st.columns([2,6,2])
with col2:
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
    sources = {
        "Google Trends": True,
        "Social Media": True,
        "Market Reports": False,
        "News Feed": True
    }
    
    for source, active in sources.items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.checkbox(source, value=active)
        with col2:
            if active:
                st.success("ativo")
            else:
                st.warning("pendente")

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Assistente IA", "📈 Análise"])

# Dashboard Tab
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tendências de Mercado")
        fig_trends = px.line(trends_data, x="month", y=["skincare", "makeup"],
                           title="Evolução de Categorias")
        st.plotly_chart(fig_trends, use_container_width=True)
        
        st.subheader("Market Share")
        fig_market = px.pie(market_data, values="value", names="name",
                          title="Participação de Mercado")
        st.plotly_chart(fig_market, use_container_width=True)
    
    with col2:
        st.subheader("Performance vs Meta")
        fig_perf = px.bar(performance_data, x="category", y=["atual", "meta"],
                         barmode="group", title="Performance por Categoria")
        st.plotly_chart(fig_perf, use_container_width=True)
        
        st.subheader("Benchmark Competitivo")
        fig_bench = px.bar(benchmark_data, x="category", 
                          y=["natura", "avon", "boticario"],
                          title="Comparativo com Concorrentes")
        st.plotly_chart(fig_bench, use_container_width=True)

# Chat Tab com Zaia
with tab2:
    st.subheader("💬 Chat com Assistente Natura")
    
    # Área de chat
    chat_container = st.container()
    
    # Exibir mensagens anteriores
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Como posso ajudar?"):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Processar com a Zaia e mostrar resposta
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Processando..."):
                response = get_zaia_response(prompt)
            message_placeholder.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Análise Tab
with tab3:
    st.subheader("Relatório Automático")
    
    with st.expander("📊 Análise de Performance"):
        st.write("Análise de performance do último trimestre:")
        st.write("• Crescimento em Skincare: +15% vs trimestre anterior")
        st.write("• Oportunidade em Makeup: -2% vs meta estabelecida")
        st.write("• Destaque para produtos coreanos: +45% em buscas")
    
    with st.expander("💡 Recomendações"):
        st.write("• Aumentar investimento em linha de Skincare")
        st.write("• Revisar estratégia de Makeup")
        st.write("• Explorar parcerias com marcas coreanas")
    
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
