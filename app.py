import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- PEGA AQUÍ TU NUEVO LINK DE GOOGLE ---
URL_API = "https://script.google.com/macros/s/AKfycbzVJV038RRhcx66xnFSCgVSLSa_-mXgu9yxT5tk_il6ehYBdhc9clRgXewcks4U_6Nf/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #FFB6C1; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    h1, h2, h3, p, label { color: #000000 !important; font-weight: bold !important; }
    div.stButton > button:first-child { background-color: #FF69B4; color: white; border-radius: 15px; width: 100%; font-weight: bold; }
    .stButton>button[kind="secondary"] { background-color: #FF4B4B; color: white; border-radius: 15px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("VK BRANDWEAR")
    menu = st.sidebar.radio("MENÚ", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"])

if menu == "INVERSIONES":
    st.title("💖 REGISTRO DE INVERSIONES")

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_in = st.date_input("FECHA", datetime.now())
            categoria = st.selectbox("CATEGORÍA", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "VESTIDOS"])
        with col2:
            prenda = st.text_input("NOMBRE PRENDA").upper()
            talla = st.selectbox("TALLA", ["XS", "S", "M", "L", "XL", "TALLA UNICA"])
        with col3:
            cantidad = st.number_input("CANTIDAD", min_value=1, step=1)
            costo_u = st.number_input("COSTO UNITARIO ($)", min_value=0.0)

    # ESPACIO PARA BOTONES
    st.write("")
    c_btn1, c_btn2, _ = st.columns([1, 1, 1])

    # INTENTAR CARGAR DATOS
    df_full = pd.DataFrame()
    try:
        res = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=10)
        if res.status_code == 200:
            datos = res.json()
            if len(datos) > 1:
                df_full = pd.DataFrame(datos[1:], columns=datos[0])
                df_full['FECHA'] = df_full['FECHA'].apply(lambda x: str(x)[:10].replace("-", "/"))
    except Exception as e:
        st.error(f"Error cargando tabla: {e}")

    with c_btn1:
        if st.button("➕ INGRESAR INVENTARIO"):
            if prenda:
                mes = MESES_ES.get(fecha_in.strftime("%B"), fecha_in.strftime("%B"))
                p_data = {
                    "action": "registrar_inversion", "fecha": str(fecha_in), "año": fecha_in.year, 
                    "mes": mes, "categoria": categoria, "prenda": prenda, 
                    "talla": talla, "cantidad": cantidad, "costo": costo_u
                }
                requests.post(URL_API, json=p_data)
                st.success("¡Guardado!")
                time.sleep(1)
                st.rerun()

    st.write("---")
    st.subheader("📋 INVENTARIO REGISTRADO")

    if not df_full.empty:
        cols = ['FECHA', 'CATEGORIA', 'NOMBRE PRENDA', 'TALLA', 'STOCK ACTUAL', 'COSTO UNITARIO', 'COSTO TOTAL']
        sel = st.dataframe(df_full, use_container_width=True, hide_index=True, column_order=cols,
                           on_select="rerun", selection_mode="multi-row",
                           column_config={"COSTO UNITARIO": st.column_config.NumberColumn("UNIT ($)", format="$ %d"),
                                         "COSTO TOTAL": st.column_config.NumberColumn("TOTAL ($)", format="$ %d")})
        
        filas = sel.selection.rows
        if filas:
            with c_btn2:
                if st.button(f"🗑️ ELIMINAR ({len(filas)})", type="secondary"):
                    for i in filas:
                        f = df_full.iloc[i]
                        requests.post(URL_API, json={"action": "eliminar_inversion", "prenda": f["NOMBRE PRENDA"], "talla": f["TALLA"], "fecha": f["FECHA"].replace("/", "-")})
                    st.rerun()
    else:
        st.info("No hay datos registrados aún.")
