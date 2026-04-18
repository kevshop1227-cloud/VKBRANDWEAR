import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN Y ESTILOS ---
URL_API = https://script.google.com/macros/s/AKfycbzVJV038RRhcx66xnFSCgVSLSa_-mXgu9yxT5tk_il6ehYBdhc9clRgXewcks4U_6Nf/exec

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

# CSS para los colores Rosado, Blanco y Letras Negritas
st.markdown(f"""
    <style>
    /* Fondo principal blanco */
    .stApp {{ background-color: #FFFFFF; }}
    
    /* Sidebar Rosado con letras blancas */
    [data-testid="stSidebar"] {{
        background-color: #FFB6C1; /* Rosado claro */
        color: white;
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

    /* Título de Marca con letra bonita */
    .brand-title {{
        font-family: 'Cursive', sans-serif;
        font-size: 45px;
        text-align: center;
        color: #FF1493;
        margin-bottom: 0px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CON LOGO Y MENÚ ---
with st.sidebar:
    # Intenta cargar el logo si está en el mismo nivel que app.py
    try:
        st.image("Logo VK NEW blanco.jpg", width=200)
    except:
        st.write("💎") # Emoji si no encuentra la imagen
    
    st.markdown('<p class="brand-title">VK BRANDWEAR</p>', unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENÚ DE CONTROL", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"])

# --- ANIMACIÓN DE CORAZONES ---
def animacion_corazones():
    # Pequeño truco para mostrar corazones
    placeholder = st.empty()
    for _ in range(3):
        placeholder.markdown("<h2 style='text-align: center;'>💖 💗 💞 💓</h2>", unsafe_allow_html=True)
        time.sleep(0.3)
        placeholder.empty()

# --- APARTADO: INVERSIONES ---
if menu == "INVERSIONES":
    animacion_corazones()
    st.title("💖 REGISTRO DE INVERSIONES")

    # Formulario de entrada
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

    # Botones de Acción
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("➕ INGRESAR INVENTARIO"):
            if prenda and categoria and talla:
                datos = {
                    "action": "registrar_inversion",
                    "fecha": str(fecha), "año": fecha.year, "mes": fecha.strftime("%B"),
                    "categoria": categoria, "prenda": prenda, "talla": talla,
                    "cantidad": cantidad, "costo": costo
                }
                res = requests.post(URL_API, json=datos)
                if res.status_code == 200:
                    st.success(f"¡{prenda} añadida al inventario!")
                    st.balloons()
            else:
                st.warning("Por favor rellena todos los campos.")

    # --- TABLA DE INVENTARIO Y ELIMINACIÓN ---
    st.write("---")
    st.subheader("📋 INVENTARIO REGISTRADO")
    
    # Leer datos de Google Sheets
    try:
        response = requests.post(URL_API, json={"action": "leer_inventario"})
        inv_data = response.json()
        df = pd.DataFrame(inv_data[1:], columns=inv_data[0])
        
        # Mostramos la tabla con posibilidad de selección
        event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="multi_row")
        
        # Lógica para eliminar
        seleccionados = event.selection.rows
        if seleccionados:
            if st.button("🗑️ ELIMINAR INVENTARIO"):
                for idx in seleccionados:
                    fila = df.iloc[idx]
                    datos_borrar = {
                        "action": "eliminar_inversion",
                        "prenda": fila["NOMBRE PRENDA"],
                        "talla": fila["TALLA"],
                        "fecha": fila["FECHA"]
                    }
                    requests.post(URL_API, json=datos_borrar)
                st.error("Registros eliminados del Excel.")
                time.sleep(1)
                st.rerun()
    except:
        st.info("Aún no hay registros o conectando con Google...")
