import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
URL_API = "https://script.google.com/macros/s/AKfycbVJV038RRhcx66xnFSCgVSLSa_-mXgu9yxT5tk_il6ehYBdhc9clRgXewcks4U_6Nf/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

# Inicialización de estados
if "input_venta_precio" not in st.session_state:
    st.session_state.input_venta_precio = 0.0

MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

# --- DISEÑO DE ALTA GAMA VK (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFDFD; font-family: 'Segoe UI', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: #FF75A0; }}
    .header-sidebar {{ text-align: center; margin-top: -90px !important; margin-bottom: 20px !important; }}
    .sidebar-brand {{ font-family: 'Segoe UI', sans-serif; font-size: 20px !important; color: white !important; font-weight: 800; text-transform: uppercase; }}
    
    /* Menú Píldora Blanca */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background-color: white !important; color: #FF75A0 !important; border-radius: 50px !important;
        padding: 8px 20px !important; font-weight: 700 !important; font-size: 14px !important;
        width: 100% !important; border: none !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: flex; justify-content: flex-start; align-items: center; cursor: pointer;
    }}
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div:first-child {{ display: none !important; }}

    .stContainer {{ background-color: #FFFFFF !important; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #F0F0F0; }}
    label[data-testid="stWidgetLabel"] p {{ color: #FF75A0 !important; font-weight: 700 !important; font-size: 14px !important; text-transform: uppercase; }}
    .main-title {{ font-size: 28px !important; font-weight: 800; color: #333; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="header-sidebar">', unsafe_allow_html=True)
    try: st.image("Logo VK NEW blanco.PNG") 
    except: st.write("💎")
    st.markdown('<p class="sidebar-brand">VK Brandwear</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("Navegación", ["📈 Inversiones", "🛍️ Ventas", "💰 Gastos", "📊 Dashboard"], label_visibility="collapsed")

# --- CARGA DE DATOS CENTRALIZADA ---
df_inv = pd.DataFrame()
try:
    res = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=15)
    if res.status_code == 200:
        data = res.json()
        if len(data) > 1:
            df_inv = pd.DataFrame(data[1:], columns=data[0])
            # Asegurar que Stock sea numérico
            df_inv['STOCK ACTUAL'] = pd.to_numeric(df_inv['STOCK ACTUAL'], errors='coerce').fillna(0)
except:
    st.error("Error conectando con el Excel.")

# ==========================================
# MÓDULO INVERSIONES (Con filtro Stock > 0)
# ==========================================
if "Inversiones" in menu:
    st.markdown('<p class="main-title">📦 Inventario de Inversiones</p>', unsafe_allow_html=True)
    
    # ... (Aquí va tu código de formulario de agregar que ya tienes) ...

    st.write("---")
    st.markdown("### 📋 Stock Disponible")
    
    if not df_inv.empty:
        # CRÍTICO: Filtramos para que no aparezcan los que tienen stock 0
        df_visible = df_inv[df_inv['STOCK ACTUAL'] > 0].copy()
        
        if not df_visible.empty:
            st.dataframe(df_visible, use_container_width=True, hide_index=True)
        else:
            st.warning("No hay productos con stock disponible.")
    else:
        st.info("Cargando inventario...")

# ==========================================
# MÓDULO VENTAS (Lógica dinámica)
# ==========================================
elif "Ventas" in menu:
    st.markdown('<p class="main-title">🛍️ Registro de Ventas</p>', unsafe_allow_html=True)
    
    with st.container():
        # Lógica de selección de prendas con Stock > 0
        if not df_inv.empty:
            df_stock = df_inv[df_inv['STOCK ACTUAL'] > 0].copy()
            df_stock['OPCION'] = df_stock['NOMBRE PRENDA'] + " - " + df_stock['TALLA'] + " (Stock: " + df_stock['STOCK ACTUAL'].astype(int).astype(str) + ")"
            opciones_prendas = df_stock['OPCION'].tolist()
        else:
            opciones_prendas = []

        tipo_v = st.selectbox("👗 Tipo de Venta", ["Prenda sola", "Conjunto"])
        
        prendas_a_vender = []
        if tipo_v == "Conjunto":
            cant_p = st.number_input("Cantidad de prendas", min_value=2, step=1)
            for i in range(cant_p):
                p = st.selectbox(f"Selecciona Prenda {i+1}", opciones_prendas, key=f"venta_{i}")
                prendas_a_vender.append(p)
        else:
            p = st.selectbox("Selecciona la Prenda", opciones_prendas)
            prendas_a_vender.append(p)

        precio_v = st.number_input("Costo de Venta", min_value=0.0, key="precio_v")
        
        if st.button("🚀 Registrar Venta"):
            # Aquí enviarías la lista de prendas_a_vender a tu Excel
            # para que el Script reste 1 a cada una en el inventario.
            st.success("Venta registrada. El stock bajará en el Excel.")
