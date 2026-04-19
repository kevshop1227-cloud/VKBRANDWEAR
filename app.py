import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
URL_API = "https://script.google.com/macros/s/AKfycbz_SRhirczh0j9V_6vglfTuugmk8ZttvPHW6e1lsjL06HxpoQONfOm_MRLW1WeF2E_9/exec"

st.set_page_config(page_title="VK BRANDWEAR", page_icon="💖", layout="wide")

# Inicialización de estados para limpieza de campos
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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {{
        background-color: #FDFDFD;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: #FF75A0; 
        color: white;
    }}

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        text-align: center !important;
        align-items: center !important;
    }}

    .logo-container {{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: -80px !important;
        margin-bottom: -10px !important;
    }}
    
    [data-testid="stSidebar"] img {{
        width: 110px !important;
    }}

    .sidebar-brand {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 24px !important;
        color: white !important;
        text-align: center !important;
        width: 100%;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 0px !important;
        margin-bottom: 25px !important;
        display: block;
        text-transform: uppercase;
    }}

    .stContainer {{
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0;
    }}
    
    .stInput input, .stSelectbox div[role="button"], .stDateInput div[data-baseweb="input"], .stNumberInput input {{
        border-radius: 12px !important;
        border: 1px solid #EEE !important;
        height: 42px !important;
        background-color: #F9F9F9 !important;
    }}

    div.stButton > button:first-child {{
        background-color: #FF75A0 !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 40px !important;
        font-weight: 600 !important;
        border: none !important;
    }}

    .stButton>button[kind="secondary"] {{
        background-color: #FF1493 !important;
        color: white !important;
        border-radius: 25px !important;
    }}

    .main-title {{
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #333;
        margin: 0 !important;
    }}
    
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
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("Logo VK NEW blanco.PNG") 
    except:
        st.write("💎")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-brand">VK Brandwear</p>', unsafe_allow_html=True)
    
    st.write("---")
    menu = st.radio("Navegación", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"], label_visibility="collapsed")

# --- CARGA DE DATOS CENTRALIZADA ---
df_full = pd.DataFrame()
df_ventas = pd.DataFrame()

try:
    # 1. Leer Inventario
    response = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=15)
    if response.status_code == 200:
        inv_data = response.json()
        if len(inv_data) > 1:
            df_full = pd.DataFrame(inv_data[1:], columns=inv_data[0])
            df_full.columns = df_full.columns.str.strip() # Limpiar nombres de columnas
            # Asegurar stock numérico
            if 'STOCK ACTUAL' in df_full.columns:
                df_full['STOCK ACTUAL'] = pd.to_numeric(df_full['STOCK ACTUAL'], errors='coerce').fillna(0)
            df_full['FECHA_RAW'] = df_full['FECHA'].astype(str).apply(lambda x: x[:10])
            df_full['FECHA'] = df_full['FECHA_RAW'].apply(lambda x: x.replace("-", "/"))
            
    # 2. Leer Ventas
    response_v = requests.post(URL_API, json={"action": "leer_ventas"}, timeout=15)
    if response_v.status_code == 200:
        v_data = response_v.json()
        if len(v_data) > 1:
            df_ventas = pd.DataFrame(v_data[1:], columns=v_data[0])
except:
    pass

# ==========================================
# MÓDULO INVERSIONES
# ==========================================
if menu == "INVERSIONES":
    col_icon, col_txt = st.columns([0.06, 0.94])
    with col_icon:
        try: st.image("INVERSIONES.png", width=45)
        except: st.write("📦")
    with col_txt:
        st.markdown('<p class="main-title">Registro de Inversiones</p>', unsafe_allow_html=True)

    st.write("")

    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1: fecha_in = st.date_input("🗓️ Fecha", datetime.now())
        with c2: prenda = st.text_input("👗 Nombre prenda", placeholder="Ej: Short Negro Lazo", key="input_prenda").upper()
        with c3: cantidad = st.number_input("📦 Cantidad", min_value=1, step=1, key="input_cantidad")
        c4, c5, c6 = st.columns(3)
        with c4: categoria = st.selectbox("🏷️ Categoría", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "VESTIDOS", "BLUSAS"], key="input_cat")
        with c5: talla = st.selectbox("📏 Talla", ["XS", "S", "M", "L", "XL", "TALLA UNICA"], key="input_talla")
        with c6: costo_u = st.number_input("💰 Costo unitario ($)", min_value=0.0, key="input_costo")
        
        if st.button("➕ AGREGAR INVENTARIO"):
            if prenda:
                with st.spinner("Registrando..."):
                    mes = MESES_ES.get(fecha_in.strftime("%B"), fecha_in.strftime("%B"))
                    datos = {"action": "registrar_inversion", "fecha": str(fecha_in), "año": fecha_in.year, "mes": mes, "categoria": categoria, "prenda": prenda, "talla": talla, "cantidad": cantidad, "costo": costo_u}
                    requests.post(URL_API, json=datos)
                    st.session_state["input_prenda"] = ""; st.session_state["input_cantidad"] = 1; st.session_state["input_costo"] = 0.0
                    st.success("¡Registrado!"); time.sleep(1); st.rerun()

    st.write("---")
    st.markdown("### 📋 Inventario Registrado")
    if not df_full.empty and 'STOCK ACTUAL' in df_full.columns:
        # FILTRO: Solo mostrar lo que tiene Stock > 0
        df_mostrar = df_full[df_full['STOCK ACTUAL'] > 0].copy()
        if not df_mostrar.empty:
            st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
            total_inv = df_mostrar['COSTO TOTAL'].astype(float).sum()
            st.markdown(f'<div class="total-card">🛍️ Total invertido en stock: ${total_inv:,.0f}</div>', unsafe_allow_html=True)
        else: st.info("No hay productos con stock disponible.")
    else: st.info("No hay registros aún.")

# ==========================================
# MÓDULO VENTAS
# ==========================================
elif menu == "VENTAS":
    col_icon, col_txt = st.columns([0.06, 0.94])
    with col_icon: st.write("🛍️")
    with col_txt: st.markdown('<p class="main-title">Registro de Ventas</p>', unsafe_allow_html=True)

    with st.container():
        v1, v2 = st.columns(2)
        with v1: fecha_v = st.date_input("🗓️ Fecha de Venta", datetime.now())
        with v2: tipo_v = st.selectbox("📝 Tipo de Venta", ["Prenda sola", "Conjunto"])

        # Preparar lista de prendas con stock
        opciones_prendas = []
        df_disponible = pd.DataFrame()
        if not df_full.empty and 'STOCK ACTUAL' in df_full.columns:
            df_disponible = df_full[df_full['STOCK ACTUAL'] > 0].copy()
            if not df_disponible.empty:
                df_disponible['LISTA'] = df_disponible['NOMBRE PRENDA'] + " - " + df_disponible['TALLA'] + " (Stock: " + df_disponible['STOCK ACTUAL'].astype(int).astype(str) + ")"
                opciones_prendas = df_disponible['LISTA'].tolist()

        prendas_seleccionadas_data = []
        
        if not opciones_prendas:
            st.warning("⚠️ No hay stock disponible para realizar ventas.")
        else:
            if tipo_v == "Prenda sola":
                p_sel = st.selectbox("🔍 Selecciona la Prenda", [""] + opciones_prendas)
                if p_sel:
                    prendas_seleccionadas_data.append(df_disponible[df_disponible['LISTA'] == p_sel].iloc[0])
            else:
                cant_p = st.number_input("🔢 Cantidad de prendas en el conjunto", min_value=2, step=1)
                c_ventas = st.columns(2)
                for i in range(cant_p):
                    with c_ventas[i % 2]:
                        p_sel = st.selectbox(f"🔍 Prenda {i+1}", [""] + opciones_prendas, key=f"venta_p_{i}")
                        if p_sel:
                            prendas_seleccionadas_data.append(df_disponible[df_disponible['LISTA'] == p_sel].iloc[0])

        st.write("---")
        v3, v4 = st.columns(2)
        with v3: 
            precio_v = st.number_input("💰 Precio de Venta ($)", min_value=0.0, key="venta_precio")
        
        # Cálculos de Negocio
        inv_calc = sum([float(p['COSTO UNITARIO']) for p in prendas_seleccionadas_data])
        ganancia = precio_v - inv_calc
        utilidad = (ganancia / precio_v * 100) if precio_v > 0 else 0

        with v4:
            st.write(f"**Inversión Total:** ${inv_calc:,.0f}")
            st.write(f"**Ganancia Real:** ${ganancia:,.0f} ({utilidad:.1f}%)")

        if st.button("🚀 REGISTRAR VENTA"):
            # Validación: todos los campos llenos
            es_valido = False
            if tipo_v == "Prenda sola" and len(prendas_seleccionadas_data) == 1: es_valido = True
            if tipo_v == "Conjunto" and len(prendas_seleccionadas_data) == cant_p: es_valido = True
            
            if es_valido and precio_v > 0:
                with st.spinner("Procesando venta..."):
                    nombre_final = " + ".join([f"{p['NOMBRE PRENDA']} {p['TALLA']}" for p in prendas_seleccionadas_data])
                    # Preparar lista para que el Excel descuente stock
                    items_descontar = [f"{p['NOMBRE PRENDA']}|{p['TALLA']}" for p in prendas_seleccionadas_data]
                    
                    datos_v = {
                        "action": "registrar_venta",
                        "fecha": str(fecha_v),
                        "prenda": nombre_final,
                        "inversion": inv_calc,
                        "venta": precio_v,
                        "ganancia": ganancia,
                        "utilidad": f"{utilidad:.1f}%",
                        "items_descontar": items_descontar
                    }
                    requests.post(URL_API, json=datos_v)
                    st.session_state.venta_precio = 0.0
                    st.success("¡Venta registrada! Stock actualizado.")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Por favor selecciona todas las prendas y el precio de venta.")

    st.write("---")
    st.markdown("### 📋 Historial de Ventas")
    if not df_ventas.empty:
        st.dataframe(df_ventas, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay ventas registradas.")
