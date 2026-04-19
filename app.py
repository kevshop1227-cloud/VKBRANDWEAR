import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
URL_API = "https://script.google.com/macros/s/AKfycbz83hP0Hfd-SCwnfAQwujomUXFILQ7PnW0DOv5JmuLNmcjXR_-puUcmecdFNqWFLho/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

# --- ESTILOS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #FFB6C1; color: white; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    h1, h2, h3, p, label { color: #000000 !important; font-weight: bold !important; }
    
    /* Botón Eliminar Estilo */
    .stButton>button[kind="secondary"] {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
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
    menu = st.radio("MENÚ DE CONTROL", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"])

# --- SECCIÓN INVERSIONES ---
if menu == "INVERSIONES":
    st.title("💖 REGISTRO DE INVERSIONES")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("FECHA", datetime.now())
            categoria = st.selectbox("CATEGORÍA", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "CAMISAS", "VESTIDOS", "PANTALONETAS", "FALDAS", "BLUSAS"])
            prenda = st.text_input("NOMBRE PRENDA").upper()
        with col2:
            talla = st.selectbox("TALLA", ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "TALLA UNICA"])
            cantidad = st.number_input("CANTIDAD", min_value=1, step=1)
            costo = st.number_input("COSTO UNITARIO ($)", min_value=0.0)

    if st.button("➕ INGRESAR INVENTARIO"):
        if prenda:
            mes_ingles = fecha.strftime("%B")
            mes_es = MESES_ES.get(mes_ingles, mes_ingles)
            datos = {
                "action": "registrar_inversion",
                "fecha": str(fecha), "año": fecha.year, "mes": mes_es,
                "categoria": categoria, "prenda": prenda, "talla": talla,
                "cantidad": cantidad, "costo": costo
            }
            requests.post(URL_API, json=datos)
            st.success("¡Registrado!")
            st.rerun()

    st.write("---")
    st.subheader("📋 INVENTARIO REGISTRADO")
    st.write("Selecciona las filas para eliminar:")

    try:
        response = requests.post(URL_API, json={"action": "leer_inventario"})
        inv_data = response.json()
        
        if len(inv_data) > 1:
            df = pd.DataFrame(inv_data[1:], columns=inv_data[0])
            
            # TABLA INTERACTIVA
            seleccion = st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True,
                on_select="rerun",
                selection_mode="multi_row",
                column_config={
                    "COSTO UNITARIO": st.column_config.NumberColumn("COSTO ($)", format="$ %d"),
                    "CANTIDAD": st.column_config.NumberColumn("CANT"),
                    "STOCK ACTUAL": st.column_config.NumberColumn("STOCK")
                }
            )

            # LÓGICA DE ELIMINACIÓN
            filas_seleccionadas = seleccion.selection.rows
            if filas_seleccionadas:
                st.warning(f"Has seleccionado {len(filas_seleccionadas)} prendas.")
                if st.button("🗑️ ELIMINAR SELECCIONADOS", type="secondary"):
                    for i in filas_seleccionadas:
                        fila = df.iloc[i]
                        # Enviamos los datos para encontrar la fila exacta en Excel
                        borrar = {
                            "action": "eliminar_inversion",
                            "prenda": fila["NOMBRE PRENDA"],
                            "talla": fila["TALLA"],
                            "fecha": str(fila["FECHA"])[:10] # Solo YYYY-MM-DD
                        }
                        requests.post(URL_API, json=borrar)
                    st.success("¡Eliminado de la App y del Excel!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("No hay datos todavía.")
    except:
        st.info("Cargando tabla...")
