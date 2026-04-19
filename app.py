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

# --- DISEÑO DE LUJO VK (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {{
        background-color: #FDFDFD;
        font-family: 'Poppins', sans-serif;
    }}
    
    /* Sidebar Rosa VK */
    [data-testid="stSidebar"] {{
        background-color: #FF75A0; 
        color: white;
    }}
    
    /* Logo de la Sidebar más pequeño */
    [data-testid="stSidebar"] img {{
        width: 120px !important;
        margin-bottom: 0px !important;
    }}
    
    /* Nombre de la marca más grande y elegante */
    .sidebar-title {{
        font-family: 'Playfair Display', serif;
        font-size: 28px !important;
        text-align: center;
        color: white !important;
        margin-top: 10px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }}

    /* Contenedores Blancos Redondeados */
    .stContainer {{
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
    }}
    
    /* UNIFORMIDAD TOTAL: Fecha, Texto, Números y Selectores */
    .stInput input, .stSelectbox div[role="button"], .stDateInput div[data-baseweb="input"], .stNumberInput input {{
        border-radius: 12px !important;
        border: 1px solid #EEE !important;
        height: 42px !important;
        background-color: #F9F9F9 !important;
        font-size: 14px !important;
    }}
    
    /* Corregir el ancho de la fecha para que no sobresalga */
    .stDateInput {{
        width: 100% !important;
    }}

    /* Botón AGREGAR (Rosa) */
    div.stButton > button:first-child {{
        background-color: #FF75A0 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 40px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(255,117,160,0.3);
    }}

    /* Botón ELIMINAR */
    .stButton>button[kind="secondary"] {{
        background-color: #FF1493 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 40px !important;
        font-weight: 600 !important;
        border: none !important;
    }}

    /* Estilo de la tabla */
    [data-testid="stDataFrame"] {{
        border-radius: 15px !important;
        border: 1px solid #F0F0F0;
    }}
    
    /* Título de sección más compacto */
    .main-header {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }}
    
    .main-header img {{
        width: 45px !important;
    }}
    
    .main-header h1 {{
        font-size: 28px !important;
        margin: 0 !important;
        padding: 0 !important;
        color: #333;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try:
        # Usamos el nombre exacto de tu GitHub
        st.image("Logo VK NEW blanco.PNG")
    except:
        st.write("💎")
    st.markdown('<p class="sidebar-title">VK BRANDWEAR</p>', unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENÚ", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"], label_visibility="collapsed")

# --- CARGA DE DATOS ---
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
if menu == "INVERSIONES":
    # Encabezado Compacto
    st.markdown(f"""
        <div class="main-header">
            <img src="https://raw.githubusercontent.com/{st.secrets.get('github_user', 'TU_USUARIO')}/{st.secrets.get('github_repo', 'TU_REPO')}/main/INVERSIONES.png" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3502/3502688.png'" style="width:45px;">
            <h1>Registro de Inversiones</h1>
        </div>
        """, unsafe_allow_html=True)

    # Formulario Simétrico
    with st.container():
        # Fila 1
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_in = st.date_input("📅 Fecha", datetime.now())
        with col2:
            prenda = st.text_input("👗 Nombre prenda", placeholder="Ej: Short Negro Lazo").upper()
        with col3:
            cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
            
        # Fila 2
        col4, col5, col6 = st.columns(3)
        with col4:
            categoria = st.selectbox("🏷️ Categoría", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "VESTIDOS", "BLUSAS"])
        with col5:
            talla = st.selectbox("📏 Talla", ["XS", "S", "M", "L", "XL", "TALLA UNICA"])
        with col6:
            costo_u = st.number_input("💰 Costo unitario ($)", min_value=0.0)
        
        st.write("")
        c_btn1, c_btn2, _ = st.columns([1, 1, 1])
        
        with c_btn1:
            if st.button("➕ AGREGAR INVENTARIO"):
                if prenda:
                    mes = MESES_ES.get(fecha_in.strftime("%B"), fecha_in.strftime("%B"))
                    datos = {"action": "registrar_inversion", "fecha": str(fecha_in), "año": fecha_in.year, "mes": mes, "categoria": categoria, "prenda": prenda, "talla": talla, "cantidad": cantidad, "costo": costo_u}
                    requests.post(URL_API, json=datos)
                    st.success("¡Registrado!")
                    time.sleep(1)
                    st.rerun()

    # Tabla de Inventario
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
        st.markdown(f'<div style="background-color: #FFF0F5; padding: 15px; border-radius: 15px; text-align: center; color: #FF75A0; font-weight: 600; border: 1px solid #FFD1DC; display: inline-block; margin-top: 20px;">🛍️ Total invertido: ${total_inv:,.0f}</div>', unsafe_allow_html=True)

        filas_selec = seleccion.selection.rows
        if filas_selec:
            with c_btn2:
                if st.button(f"🗑️ ELIMINAR ({len(filas_selec)})", type="secondary"):
                    for i in filas_selec:
                        fila = df_full.iloc[i]
                        requests.post(URL_API, json={"action": "eliminar_inversion", "prenda": fila["NOMBRE PRENDA"], "talla": fila["TALLA"], "fecha": fila["FECHA_RAW"]})
                    st.rerun()
    else:
        st.info("No hay registros aún.")
