import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard | Cancer | Data Analysis",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("./HPC_Cancer.csv")
st.sidebar.header("Filtros")

available_type = sorted(df['Descrição da Doenca'].unique())
selected_type = st.sidebar.multiselect("Tipo de Cancer", available_type, default=available_type)

available_vital = sorted(df['Status Vital'].unique())
selected_vital = st.sidebar.multiselect("Status Vital", available_vital, default=available_vital)

available_death = sorted(df['Tipo do Obito'].unique())
selected_death = st.sidebar.multiselect("Tipo do Óbito", available_death, default=available_death)

df = df[
    (df['Descrição da Doenca'].isin(selected_type)) &
    (df['Status Vital'].isin(selected_vital)) &
    (df['Tipo do Obito'].isin(selected_death))
]

st.title("Dashboard de Análise de Casos de Câncer")
st.markdown("Uma análise dos casos registrados de câncer em Poços de Caldas, de 2007 a 2018.")

st.subheader("Metricas Gerais")

if not df.empty:
    rarity = df['Indicador de Caso Raro'].value_counts()[True]
    total_records = df.shape[0]
    frequent_type = df['Descrição da Doenca'].mode()[0]
    affected_gender = df['Sexo'].mode()[0]
else:
    rarity = 0
    total_records = 0
    frequent_type = "N/A"
    affected_gender = "N/A"

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

col1.metric("Casos raros detectados", f"{rarity:,}")
col2.metric("Total de Registros", f"{total_records:,}")
col3.metric("Tipo Mais Frequente", frequent_type)
col4.metric("Genero mais Atingido", affected_gender)

st.markdown("---")

st.subheader("Graficos")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df.empty:
        top_types = df['Descrição da Doenca'].value_counts().head(10).reset_index()
        positions_graph = px.bar(
            top_types,
            x='count',
            y='Descrição da Doenca',
            orientation='h',
            title='Os 10 tipos de câncer mais frequentes',
            labels={'count': 'Descrição da Doenca'},
            color_discrete_sequence=["#B40E02"]
        )
        positions_graph.update_layout(title_x=0.3, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(positions_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de doenças.")

with col_graf2:
    if not df.empty:
        hist_graph = px.histogram(
            df,
            x='Idade',
            title='Casos por Idade',
            labels={'Idade': 'Idade', 'Casos': 'Casos'},
            color_discrete_sequence=["#B40E02"]
        )
        hist_graph.update_layout(title_x=0.4)
        st.plotly_chart(hist_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir os casos por idade.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df.empty:
        remote_count = df['Status Vital'].value_counts().reset_index()
        remote_count.columns = ['Status Vital', 'quantidade']
        remote_graph = px.pie(
            remote_count,
            values='quantidade',
            names='Status Vital',
            title='Taxa de Mortalidade (por câncer ou não)',
            labels={'Status Vital': 'Tipo de Trabalho', 'quantidade': 'Quantidade'},
            color_discrete_sequence=["#B40E02"],
            hole=0.5
        )
        remote_graph.update_traces(textposition='outside', textinfo='percent+label')
        remote_graph.update_layout(title_x=0.3)
        st.plotly_chart(remote_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de Mortalidade")

with col_graf4:
    if not df.empty:
        remote_count = df['Tipo do Obito'].value_counts().reset_index()
        remote_count.columns = ['Tipo do Obito', 'quantidade']
        remote_graph = px.pie(
            remote_count,
            values='quantidade',
            names='Tipo do Obito',
            title='Distribuição de Mortalidade',
            labels={'Tipo do Obito': 'Tipo do Obito', 'quantidade': 'Quantidade'},
            color_discrete_sequence=["#B40E02"],
            hole=0.5
        )
        remote_graph.update_traces(textposition='outside', textinfo='percent+label')
        remote_graph.update_layout(title_x=0.4)
        st.plotly_chart(remote_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de tipo de morte")

st.subheader("Dados Detalhados")
st.dataframe(df)