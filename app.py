import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN ---
URL_API = "https://script.google.com/macros/s/AKfycbz_SRhirczh0j9V_6vglfTuugmk8ZttvPHW6e1lsjL06HxpoQONfOm_MRLW1WeF2E_9/exec"

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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    .stApp {{ background-color: #FDFDFD; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: #FF75A0; color: white; }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ text-align: center !important; align-items: center !important; }}
    .logo-container {{ display: flex; justify-content: center; width: 100%; margin-top: -80px !important; margin-bottom: -10px !important; }}
    [data-testid="stSidebar"] img {{ width: 110px !important; }}
    .sidebar-brand {{ font-family: 'Segoe UI', sans-serif; font-size: 24px !important; color: white !important; font-weight: 700; letter-spacing: 1px; margin-top: 0px !important; margin-bottom: 25px !important; display: block; text-transform: uppercase; }}
    .stContainer {{ background-color: #FFFFFF; padding: 25px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #F0F0F0; }}
    .stInput input, .stSelectbox div[role="button"], .stDateInput div[data-baseweb="input"], .stNumberInput input {{ border-radius: 12px !important; border: 1px solid #EEE !important; height: 42px !important; background-color: #F9F9F9 !important; }}
    div.stButton > button:first-child {{ background-color: #FF75A0 !important; color: white !important; border-radius: 25px !important; padding: 10px 40px !important; font-weight: 600 !important; border: none !important; }}
    .stButton>button[kind="secondary"] {{ background-color: #FF1493 !important; color: white !important; border-radius: 25px !important; }}
    .main-title {{ font-size: 28px !important; font-weight: 700 !important; color: #333; margin: 0 !important; }}
    .total-card {{ background-color: #FFF0F5; padding: 12px 25px; border-radius: 15px; text-align: center; color: #FF75A0; font-weight: 600; border: 1px solid #FFD1DC; display: inline-block; margin-top: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try: st.image("Logo VK NEW blanco.PNG") 
    except: st.write("💎")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-brand">VK Brandwear</p>', unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("Navegación", ["INVERSIONES", "VENTAS", "GASTOS", "DASHBOARD"], label_visibility="collapsed")

# --- CARGA DE DATOS ---
df_full = pd.DataFrame()
df_ventas = pd.DataFrame()

try:
    # Inventario
    response = requests.post(URL_API, json={"action": "leer_inventario"}, timeout=15)
    if response.status_code == 200:
        inv_data = response.json()
        if len(inv_data) > 1:
            df_full = pd.DataFrame(inv_data[1:], columns=inv_data[0])
            df_full.columns = df_full.columns.str.strip()
            if 'STOCK ACTUAL' in df_full.columns:
                df_full['STOCK ACTUAL'] = pd.to_numeric(df_full['STOCK ACTUAL'], errors='coerce').fillna(0)
            df_full['FECHA_RAW'] = df_full['FECHA'].astype(str).apply(lambda x: x[:10])
            df_full['FECHA'] = df_full['FECHA_RAW'].apply(lambda x: x.replace("-", "/"))
            
    # Ventas
    response_v = requests.post(URL_API, json={"action": "leer_ventas"}, timeout=15)
    if response_v.status_code == 200:
        v_data = response_v.json()
        if len(v_data) > 1:
            df_ventas = pd.DataFrame(v_data[1:], columns=v_data[0])
            df_ventas.columns = df_ventas.columns.str.strip()
            df_ventas['FECHA_RAW'] = df_ventas['FECHA'].astype(str).apply(lambda x: x[:10])
except:
    pass

# --- MÓDULO INVERSIONES ---
if menu == "INVERSIONES":
    st.markdown('<p class="main-title">📦 Registro de Inversiones</p>', unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1: fecha_in = st.date_input("🗓️ Fecha", datetime.now())
        with c2: prenda = st.text_input("👗 Nombre prenda", placeholder="Ej: Short Negro Lazo", key="in_prenda").upper()
        with c3: cantidad = st.number_input("📦 Cantidad", min_value=1, step=1, key="in_cantidad")
        c4, c5, c6 = st.columns(3)
        with c4: categoria = st.selectbox("🏷️ Categoría", ["SHORTS", "TOPS", "ENTERIZOS", "BODYS", "LEGGINS", "CHAQUETAS", "VESTIDOS", "BLUSAS"], key="in_cat")
        with c5: talla = st.selectbox("📏 Talla", ["XS", "S", "M", "L", "XL", "TALLA UNICA"], key="in_talla")
        with c6: costo_u = st.number_input("💰 Costo unitario ($)", min_value=0.0, key="in_costo")
        
        btn_c1, btn_c2, _ = st.columns([1, 1, 1])
        with btn_c1:
            if st.button("➕ AGREGAR INVENTARIO"):
                if prenda:
                    with st.spinner("Registrando..."):
                        mes = MESES_ES.get(fecha_in.strftime("%B"), fecha_in.strftime("%B"))
                        datos = {"action": "registrar_inversion", "fecha": str(fecha_in), "año": fecha_in.year, "mes": mes, "categoria": categoria, "prenda": prenda, "talla": talla, "cantidad": cantidad, "costo": costo_u}
                        requests.post(URL_API, json=datos)
                        st.success("¡Registrado!")
                        time.sleep(1); st.rerun()

    st.write("---")
    st.markdown("### 📋 Inventario en Stock")
    if not df_full.empty and 'STOCK ACTUAL' in df_full.columns:
        df_mostrar = df_full[df_full['STOCK ACTUAL'] > 0].copy()
        seleccion = st.dataframe(df_mostrar, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="multi-row")
        
        if seleccion.selection.rows:
            with btn_c2:
                if st.button(f"🗑️ ELIMINAR ({len(seleccion.selection.rows)})", type="secondary"):
                    for i in seleccion.selection.rows:
                        f = df_mostrar.iloc[i]
                        requests.post(URL_API, json={"action": "eliminar_inversion", "prenda": f["NOMBRE PRENDA"], "talla": f["TALLA"], "fecha": f["FECHA_RAW"]})
                    st.rerun()
    else: st.info("Sin registros.")

# --- MÓDULO VENTAS ---
elif menu == "VENTAS":
    st.markdown('<p class="main-title">🛍️ Registro de Ventas</p>', unsafe_allow_html=True)
    with st.container():
        v1, v2 = st.columns(2)
        with v1: fecha_v = st.date_input("🗓️ Fecha Venta", datetime.now())
        with v2: tipo_v = st.selectbox("📝 Tipo", ["Prenda sola", "Conjunto"])

        opciones = []
        if not df_full.empty and 'STOCK ACTUAL' in df_full.columns:
            df_stock = df_full[df_full['STOCK ACTUAL'] > 0].copy()
            df_stock['LISTA'] = df_stock['NOMBRE PRENDA'] + " - " + df_stock['TALLA'] + " (Stock: " + df_stock['STOCK ACTUAL'].astype(int).astype(str) + ")"
            opciones = df_stock['LISTA'].tolist()

        prendas_data = []
        if not opciones: st.warning("Sin stock.")
        else:
            if tipo_v == "Prenda sola":
                p = st.selectbox("🔍 Prenda", [""] + opciones)
                if p: prendas_data.append(df_stock[df_stock['LISTA'] == p].iloc[0])
            else:
                cant = st.number_input("🔢 Cuántas prendas?", min_value=2, step=1)
                for i in range(cant):
                    p = st.selectbox(f"🔍 Prenda {i+1}", [""] + opciones, key=f"v_{i}")
                    if p: prendas_data.append(df_stock[df_stock['LISTA'] == p].iloc[0])

        st.write("---")
        v3, v4 = st.columns(2)
        with v3: p_venta = st.number_input("💰 Precio Venta ($)", min_value=0.0)
        inv = sum([float(x['COSTO UNITARIO']) for x in prendas_data])
        gan = p_venta - inv
        util = (gan / p_venta * 100) if p_venta > 0 else 0
        with v4: st.write(f"Inversión: ${inv:,.0f} | Ganancia: ${gan:,.0f} ({util:.1f}%)")

        btn_v1, btn_v2, _ = st.columns([1, 1, 1])
        with btn_v1:
            if st.button("🚀 REGISTRAR VENTA"):
                if prendas_data and p_venta > 0:
                    nom = " + ".join([f"{x['NOMBRE PRENDA']} {x['TALLA']}" for x in prendas_data])
                    desc = [f"{x['NOMBRE PRENDA']}|{x['TALLA']}" for x in prendas_data]
                    requests.post(URL_API, json={"action": "registrar_venta", "fecha": str(fecha_v), "prenda": nom, "inversion": inv, "venta": p_venta, "ganancia": gan, "utilidad": f"{util:.1f}%", "items_descontar": desc})
                    st.success("¡Venta!"); time.sleep(1); st.rerun()

    st.write("---")
    st.markdown("### 📋 Historial de Ventas")
    if not df_ventas.empty:
        seleccion_v = st.dataframe(df_ventas, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="multi-row")
        if seleccion_v.selection.rows:
            with btn_v2:
                if st.button(f"🗑️ ELIMINAR VENTA ({len(seleccion_v.selection.rows)})", type="secondary"):
                    for i in seleccion_v.selection.rows:
                        f = df_ventas.iloc[i]
                        # Enviamos datos para devolver stock
                        requests.post(URL_API, json={"action": "eliminar_venta", "fecha": f["FECHA_RAW"], "prenda_texto": f["PRENDA"], "venta": f["VENTA"]})
                    st.rerun()
    else: st.info("Sin ventas.")
