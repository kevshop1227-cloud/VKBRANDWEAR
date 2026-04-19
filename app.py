import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
# Asegúrate de que este link sea el último que generaste en Google Sheets
URL_API = "https://script.google.com/macros/s/AKfycbz83hP0Hfd-SCwnfAQwujomUXFILQ7PnW0DOv5JmuLNmcjXR_-puUcmecdFNqWFLho/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

# Diccionario para traducir meses a español
MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

# --- ESTILOS PERSONALIZADOS VK ---
st.markdown(f"""
    <style>
    /* Fondo principal blanco */
    .stApp {{ background-color: #FFFFFF; }}
    
    /* Sidebar Rosado */
    [data-testid="stSidebar"] {{
        background-color: #FFB6C1;
    }}
    [data-testid="stSidebar"] * {{ color: white !important; font-weight: bold; }}

    /* Letras en negrita y negro para el contenido */
    h1, h2, h3, p, label, .stSelectbox, .stInput {{
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* Botón Ingresar (Rosado fuerte) */
    div.stButton > button:first-child {{
        background-color: #FF69B4;
        color: white;
        border-radius: 20px;
        border: None;
    }}
    
    /* Botón de eliminar (Rojo) */
    div.stButton > button[kind="secondary"] {{
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
    }}

    /* Título de Marca */
    .brand-title {{
        font-family: 'Cursive', sans-serif;
        font-size: 40px;
        text-align: center;
        color: #FF1493;
        margin-bottom: 0px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("Logo VK NEW blanco.jpg", width=200)
    except:
        st.write("💎") # Si no encuentra el logo
    
    st.markdown('<p class="brand-title">VK BRANDWEAR</p>', unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENÚ DE CONTROL", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"])

# --- ANIMACIÓN DE CORAZONES ---
def animacion_corazones():
    placeholder = st.empty()
    for _ in range(2):
        placeholder.markdown("<h2 style='text-align: center;'>💖 💗 💞 💓</h2>", unsafe_allow_html=True)
        time.sleep(0.3)
        placeholder.empty()

# --- SECCIÓN: INVERSIONES ---
if menu == "INVERSIONES":
    animacion_corazones()
    st.title("💖 REGISTRO DE INVERSIONES")

    # Formulario
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("FECHA", datetime.now())
            categoria = st.selectbox("CATEGORÍA", 
                ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "CAMISAS", "VESTIDOS", "PANTALONETAS", "FALDAS", "BLUSAS"])
            prenda = st.text_input("NOMBRE PRENDA").upper()
        
        with col2:
            talla = st.selectbox("TALLA", ["XS", "S", "M", "L", "XL", "XXL", "XXXL", "TALLA UNICA"])
            cantidad = st.number_input("CANTIDAD", min_value=1, step=1)
            costo = st.number_input("COSTO UNITARIO ($)", min_value=0.0)

    # Botón de Registro
    if st.button("➕ INGRESAR INVENTARIO"):
        if prenda:
            mes_ingles = fecha.strftime("%B")
            mes_es = MESES_ES.get(mes_ingles, mes_ingles)
            
            datos = {
                "action": "registrar_inversion",
                "fecha": str(fecha), 
                "año": fecha.year, 
                "mes": mes_es,
                "categoria": categoria, 
                "prenda": prenda, 
                "talla": talla,
                "cantidad": cantidad, 
                "costo": costo
            }
            res = requests.post(URL_API, json=datos)
            if res.status_code == 200:
                st.success(f"¡{prenda} añadida al inventario!")
                st.balloons()
                time.sleep(1)
                st.rerun()
        else:
            st.warning("Escribe el nombre de la prenda.")

    # --- TABLA DE INVENTARIO ---
    st.write("---")
    st.subheader("📋 INVENTARIO REGISTRADO")
    st.write("Selecciona las filas que desees eliminar:")

    try:
        response = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=10)
        
        if response.status_code == 200:
            inv_data = response.json()
            
            if len(inv_data) > 1:
                df = pd.DataFrame(inv_data[1:], columns=inv_data[0])
                
                # TABLA INTERACTIVA CORREGIDA (multi-row con guion medio)
                seleccion = st.dataframe(
                    df, 
                    use_container_width=True, 
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="multi-row",
                    column_config={
                        "COSTO UNITARIO": st.column_config.NumberColumn("COSTO ($)", format="$ %d"),
                        "STOCK ACTUAL": st.column_config.NumberColumn("STOCK")
                    }
                )

                # Lógica para Eliminar
                filas_seleccionadas = seleccion.selection.rows
                if filas_seleccionadas:
                    st.warning(f"Has seleccionado {len(filas_seleccionadas)} fila(s).")
                    if st.button("🗑️ ELIMINAR SELECCIONADOS", type="secondary"):
                        with st.spinner("Eliminando de Google Sheets..."):
                            for idx in filas_seleccionadas:
                                fila = df.iloc[idx]
                                borrar = {
                                    "action": "eliminar_inversion",
                                    "prenda": fila["NOMBRE PRENDA"],
                                    "talla": fila["TALLA"],
                                    "fecha": str(fila["FECHA"])[:10]
                                }
                                requests.post(URL_API, json=borrar)
                            st.error("¡Registros eliminados!")
                            time.sleep(1)
                            st.rerun()
            else:
                st.info("El inventario está vacío.")
        else:
            st.error("No se pudo conectar con Google Sheets.")
            
    except Exception as e:
        st.info("Cargando tabla desde Google Sheets...")
