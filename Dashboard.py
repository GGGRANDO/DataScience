import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard Interativo — Análise de Jogadores")

df = pd.read_csv("database.csv")

df.columns = df.columns.str.strip()

st.sidebar.header("Filtros")

col_time = "Time"

df[col_time] = df[col_time].astype(str).str.strip()
times = sorted(df[col_time].dropna().unique().tolist())

time_escolhido = st.sidebar.selectbox(
    "Selecione o Time",
    ["Todos"] + times
)

df_filtered = df.copy()
if time_escolhido != "Todos":
    df_filtered = df_filtered[df_filtered[col_time] == time_escolhido]


numeric_cols = [
    "Gols", "Assis.", "xG", "PrgP", "Idade",
    "Cmp", "Att", "PrgC", "Min."
]

for col in numeric_cols:
    if col in df_filtered.columns:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors="coerce")

df_filtered = df_filtered.dropna(subset=["Gols", "Assis.", "xG", "PrgP"])


st.subheader("Gols por Jogador")

fig1 = px.bar(
    df_filtered,
    x="Jogador",
    y="Gols",
    color="Assis.",
    title=f"Gols por Jogador — Time: {time_escolhido}",
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Correlação entre xG e Gols")

df_filtered["PrgP"] = df_filtered["PrgP"].fillna(0)

fig2 = px.scatter(
    df_filtered,
    x="xG",
    y="Gols",
    size="PrgP",
    color="Idade",
    hover_name="Jogador",
    title="xG vs Gols (tamanho = passes progressivos)"
)
st.plotly_chart(fig2, use_container_width=True)


st.subheader("Assistências por Jogador")

fig3 = px.bar(
    df_filtered,
    x="Jogador",
    y="Assis.",
    color="xG",
    title="Assistências por Jogador"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Dados Filtrados")
st.dataframe(df_filtered)
