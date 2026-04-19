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

# --- DISEÑO DE ALTA GAMA VK (CSS) ---
st.markdown(f"""
    <style>
    /* Fuente Segoe UI General */
    .stApp {{
        background-color: #FDFDFD;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Sidebar Rosa VK */
    [data-testid="stSidebar"] {{
        background-color: #FF75A0; 
        color: white;
    }}

    /* CENTRADO DE LOGO EN SIDEBAR */
    .logo-container {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: -80px !important;
        margin-bottom: -5px !important;
    }}
    
    [data-testid="stSidebar"] img {{
        width: 110px !important;
    }}

    /* Nombre de la marca */
    .sidebar-brand {{
        font-family: 'Segoe UI', sans-serif;
        font-size: 24px !important;
        color: white !important;
        text-align: center !important;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-top: 0px !important;
        margin-bottom: 25px !important;
        text-transform: uppercase;
    }}

    /* --- ESTILO DEL MENÚ (COMO EL BOTÓN QUE PEDISTE) --- */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        gap: 15px; /* Espacio entre botones */
    }}

    /* Estilo de cada "botón" del menú */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background-color: white !important; /* Fondo blanco */
        color: #FF75A0 !important; /* Texto rosado */
        border-radius: 30px !important; /* Muy redondeado como el ejemplo */
        padding: 10px 20px !important;
        font-weight: 700 !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
    }}

    /* Ocultar el circulito feo del radio button */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div:first-child {{
        display: none !important;
    }}

    /* Alineación del texto e icono dentro del botón */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {{
        margin-left: 0px !important;
        font-size: 14px !important;
    }}

    /* Color cuando pasas el mouse (efecto hover) */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background-color: #FFF0F5 !important;
        transform: scale(1.02);
        transition: 0.2s;
    }}

    /* --- FIN ESTILO MENÚ --- */

    /* Contenedor de Apartados Blanco */
    .stContainer {{
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
    }}

    /* Nombre de los apartados del formulario (rosado) */
    label[data-testid="stWidgetLabel"] p {{
        color: #FF75A0 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        text-transform: uppercase;
    }}
    
    /* Botón AGREGAR */
    div.stButton > button:first-child {{
        background-color: #FF75A0 !important;
        color: white !important;
        border-radius: 25px !important;
        font-weight: 700 !important;
    }}

    .main-title {{
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #333;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("Logo VK NEW blanco.PNG") 
    except:
        st.write("💎")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-brand">VK Brandwear</p>', unsafe_allow_html=True)
    st.write("---")
    
    # Menú con iconos integrados al lado izquierdo
    menu = st.radio(
        "Navegación", 
        ["📈 INVERSIONES", "🛍️ VENTAS", "💰 GASTOS", "📊 DASHBOARD"], 
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
if "INVERSIONES" in menu:
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
            prenda = st.text_input("👗 Nombre prenda", placeholder="Ej: SHORT NEGRO LAZO").upper()
        with c3:
            cantidad = st.number_input("📦 Cantidad", min_value=1, step=1)
            
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
        st.markdown(f'<div style="background-color: #FFF0F5; padding: 12px 25px; border-radius: 15px; text-align: center; color: #FF75A0; font-weight: 700; border: 1px solid #FFD1DC; display: inline-block; margin-top: 20px;">🛍️ Total invertido: ${total_inv:,.0f}</div>', unsafe_allow_html=True)

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
