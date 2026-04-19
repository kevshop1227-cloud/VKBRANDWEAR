import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
# Reemplaza con tu URL de Google Apps Script
URL_API = "https://script.google.com/macros/s/AKfycbzVJV038RRhcx66xnFSCgVSLSa_-mXgu9yxT5tk_il6ehYBdhc9clRgXewcks4U_6Nf/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

MESES_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

# --- DISEÑO DE ALTA GAMA VK (CSS DEFINITIVO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Alex+Brush&family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {{
        background-color: #FDFDFD;
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* Sidebar Rosa VK */
    [data-testid="stSidebar"] {{
        background-color: #FF75A0; 
    }}

    /* Cabecera Sidebar: Logo y Nombre centrados y muy arriba */
    .header-sidebar {{
        text-align: center;
        margin-top: -100px !important;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    
    .logo-img {{
        width: 100px !important; /* Tamaño pequeño y delicado */
        margin-bottom: 0px !important;
    }}
    
    .sidebar-brand {{
        font-family: 'Alex Brush', cursive;
        font-size: 55px !important; /* Nombre bien grande */
        color: white !important;
        margin-top: -15px !important;
        margin-bottom: 30px !important;
        text-align: center;
    }}

    /* --- MENÚ DE BOTONES BLANCOS LARGOS Y REDONDEADOS --- */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        width: 100%;
    }}

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background-color: white !important;
        color: #FF75A0 !important;
        border-radius: 50px !important; /* Muy redondeados */
        padding: 10px 20px !important;
        width: 95% !important; /* Botones más largos */
        font-weight: 700 !important;
        font-size: 15px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important; /* Icono a la izquierda */
        cursor: pointer;
        transition: 0.3s;
    }}

    /* Ocultar el círculo del radio button original */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div:first-child {{
        display: none !important;
    }}

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        transform: scale(1.05);
        background-color: #FFF0F5 !important;
    }}

    /* --- ESTILO FORMULARIO --- */
    .stContainer {{
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
    }}

    label[data-testid="stWidgetLabel"] p {{
        color: #FF75A0 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }}
    
    div.stButton > button:first-child {{
        background-color: #FF75A0 !important;
        color: white !important;
        border-radius: 25px !important;
        font-weight: 700 !important;
    }}

    .main-title {{ font-size: 32px !important; font-weight: 800; color: #333; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # 1. Logo y Nombre juntos, centrados y arriba
    # Se usa st.columns para ayudar con el centrado del logo pequeño
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        try:
            st.image("Logo VK NEW blanco.PNG", use_container_width=True)
        except:
            st.write("💎")
    
    # Nombre en grande justo debajo
    st.markdown('<p class="sidebar-brand">VK Brandwear</p>', unsafe_allow_html=True)
    
    st.write("---")
    
    # 2. Menú de píldoras largas con iconos a la izquierda
    menu = st.radio(
        "Navegación", 
        ["📈 Inversiones", "🛍️ Ventas", "💰 Gastos", "🔄 Reinversiones", "📊 Dashboard"], 
        label_visibility="collapsed"
    )

# --- LÓGICA DE CARGA DE DATOS ---
df_full = pd.DataFrame()
try:
    response = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=15)
    if response.status_code == 200:
        inv_data = response.json()
        if len(inv_data) > 1:
            df_full = pd.DataFrame(inv_data[1:], columns=inv_data[0])
            df_full['FECHA_RAW'] = df_full['FECHA'].astype(str).apply(lambda x: x[:10])
            df_full['FECHA'] = df_full['FECHA_RAW'].apply(lambda x: x.replace("-", "/"))
except:
    pass

# --- MÓDULO INVERSIONES ---
if "Inversiones" in menu:
    col_icon, col_txt = st.columns([0.06, 0.94])
    with col_icon:
        try:
            st.image("INVERSIONES.png", width=45)
        except:
            st.write("📁")
    with col_txt:
        st.markdown('<p class="main-title">Registro de Inversiones</p>', unsafe_allow_html=True)

    st.write("")

    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            fecha_in = st.date_input("🗓️ Fecha", datetime.now())
        with c2:
            prenda = st.text_input("👗 Nombre prenda", placeholder="EJ: SHORT BLANCO").upper()
        with c3:
            cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
            
        c4, c5, c6 = st.columns(3)
        with c4:
            categoria = st.selectbox("🏷️ Categoría", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "VESTIDOS", "BLUSAS"])
        with c5:
            talla = st.selectbox("📏 Talla", ["XS", "S", "M", "L", "XL", "TALLA UNICA"])
        with c6:
            costo_u = st.number_input("💰 Costo unitario ($)", min_value=0.0)
        
        st.write("")
        btn_c1, btn_c2, _ = st.columns([1, 1, 1])
        
        with btn_c1:
            if st.button("➕ AGREGAR INVENTARIO"):
                if prenda:
                    mes = MESES_ES.get(fecha_in.strftime("%B"), fecha_in.strftime("%B"))
                    datos = {"action": "registrar_inversion", "fecha": str(fecha_in), "año": fecha_in.year, "mes": mes, "categoria": categoria, "prenda": prenda, "talla": talla, "cantidad": cantidad, "costo": costo_u}
                    requests.post(URL_API, json=datos)
                    st.success("¡Registrado!")
                    time.sleep(1)
                    st.rerun()

    # Tabla
    st.write("---")
    st.markdown("### 📋 Inventario Registrado")
    
    if not df_full.empty:
        cols_mostrar = ['FECHA', 'CATEGORIA', 'NOMBRE PRENDA', 'TALLA', 'STOCK ACTUAL', 'COSTO UNITARIO', 'COSTO TOTAL']
        seleccion = st.dataframe(
            df_full,
            use_container_width=True,
            hide_index=True,
            column_order=cols_mostrar,
            on_select="rerun",
            selection_mode="multi-row",
            column_config={
                "FECHA": st.column_config.DateColumn("Fecha", format="YYYY/MM/DD"),
                "COSTO UNITARIO": st.column_config.NumberColumn("Unit ($)", format="$ %d"),
                "COSTO TOTAL": st.column_config.NumberColumn("Total ($)", format="$ %d")
            }
        )

        total_inv = df_full['COSTO TOTAL'].sum()
        st.markdown(f'<div style="background-color: #FFF0F5; padding: 12px 25px; border-radius: 15px; text-align: center; color: #FF75A0; font-weight: 700; border: 1px solid #FFD1DC; display: inline-block; margin-top: 20px;">🛍️ Total invertido: ${total_inv:,.0f}</div>', unsafe_allow_html=True)

        filas_selec = seleccion.selection.rows
        if filas_selec:
            with btn_c2:
                if st.button(f"🗑️ ELIMINAR ({len(filas_selec)})", type="secondary"):
                    for i in filas_selec:
                        fila = df_full.iloc[i]
                        requests.post(URL_API, json={"action": "eliminar_inversion", "prenda": fila["NOMBRE PRENDA"], "talla": fila["TALLA"], "fecha": fila["FECHA_RAW"]})
                    st.rerun()
