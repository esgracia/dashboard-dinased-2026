import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Dashboard DINASED", layout="wide")

# Título del Dashboard
st.title("🚨 Panel de Control Táctico - Personas Desaparecidas (Ecuador 2026)")
st.markdown("Herramienta de análisis espacial y demográfico para la reasignación de recursos operativos.")

# 1. Cargar los datos limpios
@st.cache_data
def cargar_datos():
    df = pd.read_csv('desaparecidos_limpio.csv')
    df = df.rename(columns={'latitud': 'LAT', 'longitud': 'LON'})
    return df

df = cargar_datos()

# 2. Barra lateral para Filtros Interactivos
st.sidebar.header("Filtros de Búsqueda")
provincia_sel = st.sidebar.selectbox("Seleccione la Provincia:", ["Todas"] + sorted(df['provincia'].dropna().unique().tolist()))
rango_edad_sel = st.sidebar.selectbox("Rango de Edad:", ["Todos"] + sorted(df['rango_edad'].dropna().unique().tolist()))

# Aplicar filtros
df_filtrado = df.copy()
if provincia_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['provincia'] == provincia_sel]
if rango_edad_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['rango_edad'] == rango_edad_sel]

# 3. Tarjetas de Indicadores Clave (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total de Casos Filtrados", value=f"{df_filtrado.shape[0]:,}")
with col2:
    en_investigacion = df_filtrado[df_filtrado['status'] == 'EN INVESTIGACIÓN'].shape[0]
    pct_investigacion = (en_investigacion / df_filtrado.shape[0]) * 100 if df_filtrado.shape[0] > 0 else 0
    st.metric(label="Casos en Investigación", value=f"{pct_investigacion:.1f}%")
with col3:
    if 'dias_demora_denuncia' in df_filtrado.columns:
        demora_promedio = df_filtrado['dias_demora_denuncia'].mean()
        st.metric(label="Demora Promedio en Denunciar", value=f"{demora_promedio:.1f} días")
    else:
        st.metric(label="Demora Promedio en Denunciar", value="N/A")

# 4. Mapa Georreferenciado
st.subheader("📍 Mapa de Calor Operativo")
st.markdown("Visualización de las coordenadas exactas de las desapariciones para despliegue de patrullas.")
df_mapa = df_filtrado.dropna(subset=['LAT', 'LON'])
st.map(df_mapa)

# 5. Análisis Demográfico
st.subheader("📊 Perfil Demográfico de las Víctimas")
colA, colB = st.columns(2)

with colA:
    st.markdown("**Distribución por Sexo**")
    st.bar_chart(df_filtrado['sexo'].value_counts())

with colB:
    st.markdown("**Distribución por Rango de Edad**")
    st.bar_chart(df_filtrado['rango_edad'].value_counts())