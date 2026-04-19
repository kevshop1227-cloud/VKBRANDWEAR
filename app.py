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

# --- DISEÑO LIMPIO VK (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {{
        background-color: #FDFDFD;
        font-family: 'Poppins', sans-serif;
    }}
    
    /* Sidebar Rosa VK */
    [data-testid="stSidebar"] {{
        background-color: #FF75A0; 
        color: white;
    }}
    [data-testid="stSidebar"] * {{ color: white !important; font-weight: 600; }}
    
    .sidebar-title {{
        font-size: 24px;
        text-align: center;
        font-weight: 600;
        margin-top: -10px;
    }}

    /* Contenedores Blancos Redondeados */
    .stContainer {{
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
    }}
    
    /* Inputs uniformes y del mismo tamaño */
    .stInput input, .stSelectbox div[role="button"], .stDateInput div, .stNumberInput input {{
        border-radius: 12px !important;
        border: 1px solid #EEE !important;
        padding: 10px !important;
        height: 45px !important;
    }}

    /* Botón AGREGAR (Rosa) */
    div.stButton > button:first-child {{
        background-color: #FF75A0 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 40px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(255,117,160,0.3);
    }}

    /* Botón ELIMINAR (Rosa fuerte) */
    .stButton>button[kind="secondary"] {{
        background-color: #FF1493 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 40px !important;
        font-weight: 600 !important;
        border: none !important;
    }}

    /* Tabla Estilizada */
    [data-testid="stDataFrame"] {{
        border-radius: 15px !important;
        overflow: hidden !important;
    }}
    
    .total-card {{
        background-color: #FFF0F5;
        padding: 15px 30px;
        border-radius: 15px;
        text-align: center;
        color: #FF75A0;
        font-weight: 600;
        margin-top: 20px;
        border: 1px solid #FFD1DC;
        display: inline-block;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try:
        # Corregido a .PNG como en tu imagen
        st.image("Logo VK NEW blanco.PNG", use_container_width=True)
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
    # Encabezado con imagen corregida a .png minúscula
    col_h1, col_h2 = st.columns([0.15, 0.85])
    with col_h1:
        try:
            st.image("INVERSIONES.png", width=80)
        except:
            st.write("📁")
    with col_h2:
        st.markdown("<h1 style='margin-bottom:0; font-size: 38px;'>Registro de Inversiones</h1>", unsafe_allow_html=True)

    st.write("") 

    # Formulario con columnas uniformes
    with st.container():
        # Fila 1: Fecha, Nombre y Cantidad (Mismo tamaño)
        f1_c1, f1_c2, f1_c3 = st.columns(3)
        with f1_c1:
            fecha_in = st.date_input("🗓️ Fecha", datetime.now())
        with f1_c2:
            prenda = st.text_input("👗 Nombre prenda", placeholder="Ej: Short Negro Lazo").upper()
        with f1_c3:
            cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
            
        # Fila 2: Categoría, Talla y Costo
        f2_c1, f2_c2, f2_c3 = st.columns(3)
        with f2_c1:
            categoria = st.selectbox("🏷️ Categoría", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "VESTIDOS", "BLUSAS"])
        with f2_c2:
            talla = st.selectbox("📏 Talla", ["XS", "S", "M", "L", "XL", "TALLA UNICA"])
        with f2_c3:
            costo_u = st.number_input("💰 Costo unitario ($)", min_value=0.0)
        
        st.write("")
        c_btn1, c_btn2, _ = st.columns([1, 1, 1])
        
        with c_btn1:
            if st.button("➕ AGREGAR INVENTARIO"):
                if prenda:
                    mes = MESES_ES.get(fecha_in.strftime("%B"), fecha_in.strftime("%B"))
                    datos = {"action": "registrar_inversion", "fecha": str(fecha_in), "año": fecha_in.year, "mes": mes, "categoria": categoria, "prenda": prenda, "talla": talla, "cantidad": cantidad, "costo": costo_u}
                    requests.post(URL_API, json=datos)
                    st.success("¡Agregado!")
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
        st.markdown(f'<div class="total-card">🛍️ Total invertido: ${total_inv:,.0f}</div>', unsafe_allow_html=True)

        filas_selec = seleccion.selection.rows
        if filas_selec:
            with c_btn2:
                if st.button(f"🗑️ ELIMINAR ({len(filas_selec)})", type="secondary"):
                    for i in filas_selec:
                        fila = df_full.iloc[i]
                        requests.post(URL_API, json={"action": "eliminar_inversion", "prenda": fila["NOMBRE PRENDA"], "talla": fila["TALLA"], "fecha": fila["FECHA_RAW"]})
                    st.rerun()
    else:
        st.info("No hay registros en el inventario.")
