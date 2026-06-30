import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# CONFIGURACIÓN DE LA PÁGINA
# ===============================
st.set_page_config(
    page_title="Dashboard de Gestión de Citas Médicas",
    page_icon="🏥",
    layout="wide"
)

# ===============================
# CARGA DE DATOS
# ===============================
df = pd.read_csv("citas_medicas.csv")

df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.month

# ===============================
# TÍTULO
# ===============================
st.title("🏥 Dashboard de Gestión de Citas Médicas")
st.markdown("### Hospital de Lima Norte")
st.write("Sistema de análisis de citas médicas mediante Business Intelligence y Big Data.")

st.markdown("---")

# ===============================
# MÉTRICAS
# ===============================

total_citas = len(df)
total_especialidades = df["especialidad"].nunique()
edad_promedio = round(df["edad"].mean(),1)
canceladas = (df["estado"]=="Cancelada").sum()

col1,col2,col3,col4 = st.columns(4)

col1.metric("📅 Total de Citas", total_citas)
col2.metric("🏥 Especialidades", total_especialidades)
col3.metric("👨 Edad Promedio", edad_promedio)
col4.metric("❌ Canceladas", canceladas)

st.markdown("---")

# ===============================
# PRIMERA FILA
# ===============================

col1,col2 = st.columns(2)

with col1:

    st.subheader("📊 Citas por Especialidad")

    especialidades = (
        df["especialidad"]
        .value_counts()
        .reset_index()
    )

    especialidades.columns = ["Especialidad","Cantidad"]

    fig1 = px.bar(
        especialidades,
        x="Especialidad",
        y="Cantidad",
        color="Especialidad",
        text_auto=True
    )

    fig1.update_layout(showlegend=False)

    st.plotly_chart(fig1,use_container_width=True)

with col2:

    st.subheader("🥧 Estado de las Citas")

    fig2 = px.pie(
        df,
        names="estado",
        hole=0.45
    )

    fig2.update_traces(textinfo="percent+label")

    st.plotly_chart(fig2,use_container_width=True)

st.markdown("---")

# ===============================
# SEGUNDA FILA
# ===============================

st.subheader("📈 Evolución de Citas por Mes")

citas_mes = (
    df.groupby("mes")
    .size()
    .reset_index(name="Cantidad")
)

fig3 = px.line(
    citas_mes,
    x="mes",
    y="Cantidad",
    markers=True
)

fig3.update_layout(
    xaxis_title="Mes",
    yaxis_title="Cantidad de Citas"
)

st.plotly_chart(fig3,use_container_width=True)

st.markdown("---")

# ===============================
# TABLA
# ===============================

st.subheader("📋 Vista previa del Dataset")

st.dataframe(
    df,
    use_container_width=True
)