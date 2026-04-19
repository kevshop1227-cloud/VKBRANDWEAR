import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
URL_API = "https://script.google.com/macros/s/AKfycbzVJV038RRhcx66xnFSCgVSLSa_-mXgu9yxT5tk_il6ehYBdhc9clRgXewcks4U_6Nf/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #FFB6C1; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    h1, h2, h3, p, label { color: #000000 !important; font-weight: bold !important; }
    
    div.stButton > button:first-child {
        background-color: #FF69B4;
        color: white;
        border-radius: 15px;
        width: 100%;
        font-weight: bold;
    }
    
    .stButton>button[kind="secondary"] {
        background-color: #FF4B4B;
        color: white;
        border-radius: 15px;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("Logo VK NEW blanco.jpg", width=200)
    except:
        st.write("💎")
    st.title("VK BRANDWEAR")
    menu = st.sidebar.radio("MENÚ DE CONTROL", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"])

if menu == "INVERSIONES":
    st.title("💖 REGISTRO DE INVERSIONES")

    # 1. Formulario
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_input = st.date_input("FECHA", datetime.now())
            categoria = st.selectbox("CATEGORÍA", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "CAMISAS", "VESTIDOS", "PANTALONETAS", "FALDAS", "BLUSAS"])
        with col2:
            prenda = st.text_input("NOMBRE PRENDA").upper()
            talla = st.selectbox("TALLA", ["XS", "S", "M", "L", "XL", "TALLA UNICA"])
        with col3:
            cantidad = st.number_input("CANTIDAD", min_value=1, step=1)
            costo_u = st.number_input("COSTO UNITARIO ($)", min_value=0.0)

    # --- LECTURA DE DATOS DESDE EXCEL ---
    try:
        response = requests.post(URL_API, json={"action": "leer_inventario"})
        inv_data = response.json()
        if len(inv_data) > 1:
            # Ahora el DataFrame carga automáticamente la columna "COSTO TOTAL" desde el Excel
            df_full = pd.DataFrame(inv_data[1:], columns=inv_data[0])
            df_full['FECHA'] = df_full['FECHA'].apply(lambda x: str(x)[:10].replace("-", "/"))
        else:
            df_full = pd.DataFrame()
    except:
        df_full = pd.DataFrame()

    # 2. FILA DE BOTONES
    st.write("")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("➕ INGRESAR INVENTARIO"):
            if prenda:
                mes_es = MESES_ES.get(fecha_input.strftime("%B"), fecha_input.strftime("%B"))
                datos = {
                    "action": "registrar_inversion",
                    "fecha": str(fecha_input), "año": fecha_input.year, "mes": mes_es,
                    "categoria": categoria, "prenda": prenda, "talla": talla,
                    "cantidad": cantidad, "costo": costo_u
                }
                requests.post(URL_API, json=datos)
                st.success("¡Guardado en Excel!")
                time.sleep(1)
                st.rerun()

    # 3. TABLA Y ELIMINACIÓN
    st.write("---")
    st.subheader("📋 INVENTARIO REGISTRADO")

    if not df_full.empty:
        # Aquí definimos el orden exacto incluyendo la nueva columna que viene del Excel
        cols_mostrar = ['FECHA', 'CATEGORIA', 'NOMBRE PRENDA', 'TALLA', 'STOCK ACTUAL', 'COSTO UNITARIO', 'COSTO TOTAL']
        
        seleccion = st.dataframe(
            df_full,
            use_container_width=True,
            hide_index=True,
            column_order=cols_mostrar,
            on_select="rerun",
            selection_mode="multi-row",
            column_config={
                "COSTO UNITARIO": st.column_config.NumberColumn("UNITARIO ($)", format="$ %d"),
                "COSTO TOTAL": st.column_config.NumberColumn("TOTAL ($)", format="$ %d"),
                "STOCK ACTUAL": "STOCK"
            }
        )

        # Botón de Eliminar dinámico
        filas_selec = seleccion.selection.rows
        if filas_selec:
            with col_btn2:
                if st.button(f"🗑️ ELIMINAR ({len(filas_selec)})", type="secondary"):
                    for i in filas_selec:
                        fila = df_full.iloc[i]
                        borrar = {
                            "action": "eliminar_inversion",
                            "prenda": fila["NOMBRE PRENDA"],
                            "talla": fila["TALLA"],
                            "fecha": fila["FECHA"].replace("/", "-")
                        }
                        requests.post(URL_API, json=borrar)
                    st.rerun()
    else:
        st.info("No hay registros aún.")
