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

# ==========================================
# 2. LISTA DE PERSONAL MÁSTER
# ==========================================
PERSONAL = ["Sofia", "Esmeralda", "Luz", "Jenny", "Nicol", "Kenia", "Leyver"]

# ==========================================
# 3. CONTROL DE SESIÓN POR URL (ANTI-RELOAD)
# ==========================================
url_params = st.query_params
usuario_en_url = url_params.get("usuario", None)

# Determinamos qué posición debe tomar el selector por defecto
index_defecto = 0
if usuario_en_url in PERSONAL:
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
    if usuario_sel == "Leyver":
        st.warning("📍 **Asignación Fija:** 3B2 Pueblo Nuevo únicamente.")
    
    st.info(f"Aquí se muestran las coberturas asignadas para esta semana a **{usuario_sel}**.")
    
    # Espacio para tus datos, tablas o textos de los turnos:
    st.write("### Horarios de la semana:")
    
    # Botón para cerrar sesión o cambiar de usuario
    st.write("---")
    if st.button("🚪 Cambiar de Usuario / Salir", use_container_width=True):
        st.query_params.clear()
        st.rerun()

else:
    # Si vuelven a poner la opción por defecto, limpiamos la URL
    st.query_params.clear()
    
    st.info("👋 Bienvenida/o. Por favor selecciona tu nombre en la barra de arriba para ver tus turnos asignados.")
