import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
# Asegúrate de que este link sea el último que copiaste al hacer la "Nueva Versión"
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
    [data-testid="stSidebar"] { background-color: #FFB6C1; }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    h1, h2, h3, p, label { color: #000000 !important; font-weight: bold !important; }
    div.stButton > button:first-child {
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
        border: None;
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
            time.sleep(1)
            st.rerun()

    st.write("---")
    st.subheader("📋 INVENTARIO REGISTRADO")

    # --- LÓGICA DE CARGA DE TABLA CON DETECTOR DE ERRORES ---
    try:
        response = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=10)
        
        if response.status_code == 200:
            inv_data = response.json()
            if len(inv_data) > 1:
                df = pd.DataFrame(inv_data[1:], columns=inv_data[0])
                
                # Tabla interactiva
                seleccion = st.dataframe(
                    df, 
                    use_container_width=True, 
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="multi_row",
                    column_config={
                        "COSTO UNITARIO": st.column_config.NumberColumn("COSTO ($)", format="$ %d"),
                        "STOCK ACTUAL": st.column_config.NumberColumn("STOCK")
                    }
                )

                # Botón de eliminar (solo si hay selección)
                filas_seleccionadas = seleccion.selection.rows
                if filas_seleccionadas:
                    if st.button("🗑️ ELIMINAR SELECCIONADOS"):
                        for i in filas_seleccionadas:
                            fila = df.iloc[i]
                            borrar = {
                                "action": "eliminar_inversion",
                                "prenda": fila["NOMBRE PRENDA"],
                                "talla": fila["TALLA"],
                                "fecha": str(fila["FECHA"])[:10]
                            }
                            requests.post(URL_API, json=borrar)
                        st.success("¡Eliminado!")
                        time.sleep(1)
                        st.rerun()
            else:
                st.info("El Excel está vacío. Registra tu primera prenda arriba.")
        else:
            st.error(f"Error de conexión: {response.status_code}")
            
    except Exception as e:
        st.warning("Asegúrate de haber implementado la 'Nueva versión' en Google Apps Script.")
        st.error(f"Detalle técnico: {e}")
