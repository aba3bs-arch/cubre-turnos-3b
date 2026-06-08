import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN COMPLETA Y BLINDADA
# ==========================================
st.set_page_config(
    page_title="Control de Turnos - 3B", 
    page_icon="📋", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS inyectados para mejorar la experiencia en celulares (pantallas chicas)
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .stSelectbox label { font-size: 1.1rem; font-weight: bold; }
    </style>
""", unsafe_allowed_html=True)

# ==========================================
# 2. LISTA DE PERSONAL MÁSTER
# ==========================================
# Modifica o añade nombres aquí según lo necesites
PERSONAL = ["Sofia", "Esmeralda", "Luz", "Jenny", "Nicol", "Kenia", "Leyver"]

# ==========================================
# 3. CONTROL DE SESIÓN POR URL (ANTI-RELOAD)
# ==========================================
# Leemos si ya existe un usuario en el enlace del navegador
url_params = st.query_params
usuario_en_url = url_params.get("usuario", None)

# Determinamos qué posición debe tomar el selector por defecto
index_defecto = 0
if usuario_en_url in PERSONAL:
    # Sumamos 1 porque la posición 0 es el mensaje de bienvenida
    index_defecto = PERSONAL.index(usuario_en_url) + 1

# ==========================================
# 4. INTERFAZ PRINCIPAL (SELECTOR)
# ==========================================
st.title("📋 Control de Turnos 3B")
st.write("---")

usuario_sel = st.selectbox(
    "¿Quién eres? Selecciona tu nombre:",
    options=["-- Selecciona tu nombre de la lista --"] + PERSONAL,
    index=index_defecto
)

# ==========================================
# 5. LÓGICA DE DESPLIEGUE POR USUARIO
# ==========================================
if usuario_sel != "-- Selecciona tu nombre de la lista --":
    # Guardamos el usuario en la URL inmediatamente
    st.query_params["usuario"] = usuario_sel
    
    st.success(f"Sesión activa: **{usuario_sel}**")
    st.subheader(f"📅 Mi Panel de Coberturas")
    
    # ---------------------------------------------------------
    # REGLAS E INFORMACIÓN ESPECÍFICA POR USUARIO
    # ---------------------------------------------------------
    
    # Caso especial: Leyver (Restringido a su sucursal única)
    if usuario_sel == "Leyver":
        st.warning("📍 **Asignación Fija:** 3B2 Pueblo Nuevo únicamente.")
    
    # Espacio seguro para meter la visualización de tus turnos:
    st.info(f"Aquí se muestran las coberturas asignadas para esta semana a **{usuario_sel}**.")
    
    # Ejemplo de estructura de datos local para mostrar algo en pantalla (puedes cambiarlo)
    st.write("### Horarios de la semana:")
    # Aquí puedes meter tus st.dataframe(), st.table() o los textos de los turnos.
    
    # Botón para cerrar sesión o cambiar de usuario limpiando la URL
    st.write("---")
    if st.button("🚪 Cambiar de Usuario / Salir", use_container_width=True):
        st.query_params.clear()
        st.rerun()

else:
    # Si vuelven a poner la opción por defecto, limpiamos la URL
    st.query_params.clear()
    
    st.info("👋 Bienvenida/o. Por favor selecciona tu nombre en la barra de arriba para ver tus turnos asignados.")
    st.caption("Nota: Una vez que te selecciones, puedes recargar la página o cerrar el navegador y la app recordará tu sesión.")
