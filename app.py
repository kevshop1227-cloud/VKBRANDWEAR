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
    /* Importar Fuentes: Poppins y Alex Brush (Opción A) */
    @import url('https://fonts.googleapis.com/css2?family=Alex+Brush&family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {{
        background-color: #FDFDFD;
        font-family: 'Poppins', sans-serif;
    }}
    
    /* Sidebar Rosa VK */
    [data-testid="stSidebar"] {{
        background-color: #FF75A0; 
        color: white;
    }}

    /* CENTRADO DE SIDEBAR */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        text-align: center !important;
        align-items: center !important;
    }}

    /* Contenedor del Logo: Arriba y Centrado */
    .logo-container {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: -50px !important; /* Sube el logo al tope */
        margin-bottom: 0px !important;
    }}
    
    [data-testid="stSidebar"] img {{
        width: 115px !important;
    }}

    /* Nombre de la marca: Debajo del logo, fuente Alex Brush */
    .sidebar-brand {{
        font-family: 'Alex Brush', cursive;
        font-size: 42px !important;
        color: white !important;
        text-align: center !important;
        width: 100%;
        margin-top: -10px !important;
        margin-bottom: 20px !important;
        display: block;
    }}

    /* Contenedores Blancos Redondeados */
    .stContainer {{
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
    }}
    
    /* UNIFORMIDAD DE INPUTS: Misma altura y estilo */
    .stInput input, .stSelectbox div[role="button"], .stDateInput div[data-baseweb="input"], .stNumberInput input {{
        border-radius: 12px !important;
        border: 1px solid #EEE !important;
        height: 42px !important;
        background-color: #F9F9F9 !important;
    }}

    /* Botones Estilizados */
    div.stButton > button:first-child {{
        background-color: #FF75A0 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 40px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(255,117,160,0.3);
    }}

    .stButton>button[kind="secondary"] {{
        background-color: #FF1493 !important;
        color: white !important;
        border-radius: 25px !important;
    }}

    /* Encabezado Principal Compacto */
    .header-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
    }}
    
    .header-container img {{
        width: 40px !important;
    }}
    
    .header-container h1 {{
        font-size: 28px !important;
        color: #333;
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* Card del Total Invertido */
    .total-card {{
        background-color: #FFF0F5;
        padding: 12px 25px;
        border-radius: 15px;
        text-align: center;
        color: #FF75A0;
        font-weight: 600;
        border: 1px solid #FFD1DC;
        display: inline-block;
        margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # 1. Logo (Al tope y centrado)
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("Logo VK NEW blanco.PNG") 
    except:
        st.write("💎")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Nombre de la marca (Debajo del logo, fuente cursiva)
    st.markdown('<p class="sidebar-brand">VK Brandwear</p>', unsafe_allow_html=True)
    
    st.write("---")
    menu = st.radio("Navegación", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"], label_visibility="collapsed")

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
    # Título con icono pequeño y pegado
    st.markdown(f"""
        <div class="header-container">
            <img src="https://raw.githubusercontent.com/{st.secrets.get('github_user', 'TU_USER')}/{st.secrets.get('github_repo', 'TU_REPO')}/main/INVERSIONES.png" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3502/3502688.png'">
            <h1>Registro de Inversiones</h1>
        </div>
        """, unsafe_allow_html=True)

    # Formulario Symmetrical (3 columnas x 2 filas)
    with st.container():
        # Fila 1
        c1, c2, c3 = st.columns(3)
        with c1:
            fecha_in = st.date_input("🗓️ Fecha", datetime.now())
        with c2:
            prenda = st.text_input("👗 Nombre prenda", placeholder="Ej: Short Negro Lazo").upper()
        with c3:
            cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
            
        # Fila 2
        c4, c5, c6 = st.columns(3)
        with c4:
            categoria = st.selectbox("🏷️ Categoría", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "VESTIDOS", "BLUSAS"])
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
        st.markdown(f'<div class="total-card">🛍️ Total invertido: ${total_inv:,.0f}</div>', unsafe_allow_html=True)

        filas_selec = seleccion.selection.rows
        if filas_selec:
            with btn_c2:
                if st.button(f"🗑️ ELIMINAR ({len(filas_selec)})", type="secondary"):
                    for i in filas_selec:
                        fila = df_full.iloc[i]
                        requests.post(URL_API, json={"action": "eliminar_inversion", "prenda": fila["NOMBRE PRENDA"], "talla": fila["TALLA"], "fecha": fila["FECHA_RAW"]})
                    st.rerun()
    else:
        st.info("No hay registros aún.")
