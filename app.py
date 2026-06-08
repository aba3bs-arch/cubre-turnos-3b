import streamlit as st
import pandas as pd
import time
import os
import requests  # Librería nativa para conectar con el buzón en internet

# --- CONFIGURACIÓN DE LA PÁGINA (Icono oficial logo3b.png) ---
logo_path = "logo3b.png"
if os.path.exists(logo_path):
    st.set_page_config(page_title="Las 3B - Roles", page_icon=logo_path, layout="wide", initial_sidebar_state="collapsed")
else:
    st.set_page_config(page_title="Las 3B - Roles", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILOS VISUALES (Punto rojo parpadeante) ---
st.markdown("""
    <style>
    .badge-red { 
        height: 18px; width: 18px; background-color: #ff4b4b; 
        border-radius: 50%; display: inline-block; animation: pulse 1s infinite; 
    }
    @keyframes pulse { 
        0% { transform: scale(0.9); opacity: 1; } 
        70% { transform: scale(1.3); opacity: 0.7; } 
        100% { transform: scale(0.9); opacity: 1; } 
    }
    </style>
    """, unsafe_allow_html=True)

def play_alarm_sound():
    audio_html = """
        <audio autoplay loop id="alarm-audio">
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 1. INICIALIZACIÓN DE SUCURSALES Y PERSONAL ---
if "descansos_tiendas" not in st.session_state:
    st.session_state.descansos_tiendas = [
        {"Tienda": "Fusión", "Turno": "Día", "Día Descanso": "Domingo"},
        {"Tienda": "Fusión", "Turno": "Noche", "Día Descanso": "Miércoles"},
        {"Tienda": "3B2 Pueblo Nuevo", "Turno": "Día", "Día Descanso": "Domingo"},
        {"Tienda": "3B2 Pueblo Nuevo", "Turno": "Noche", "Día Descanso": "Jueves"},
        {"Tienda": "3B5 Lomas Dos", "Turno": "Día", "Día Descanso": "Viernes"},
        {"Tienda": "3B5 Lomas Dos", "Turno": "Noche", "Día Descanso": "Martes"},
        {"Tienda": "3B6 Solidaridad", "Turno": "Día", "Día Descanso": "Martes"},
        {"Tienda": "3B6 Solidaridad", "Turno": "Noche", "Día Descanso": "Jueves"},
        {"Tienda": "3B7 Col del Valle", "Turno": "Día", "Día Descanso": "Miércoles"},
        {"Tienda": "3B7 Col del Valle", "Turno": "Noche", "Día Descanso": "Viernes"},
        {"Tienda": "3B10 El Mezquite", "Turno": "Día", "Día Descanso": "Sábado"},
        {"Tienda": "3B10 El Mezquite", "Turno": "Día", "Día Descanso": "Domingo"},
        {"Tienda": "3B10 El Mezquite", "Turno": "Noche", "Día Descanso": "Lunes"},
    ]

if "personal" not in st.session_state:
    st.session_state.personal = {
        "Sofía": ["Día", "Noche"],
        "Esmeralda": ["Día", "Noche"],
        "Luz": ["Domingo Día"],
        "Jenny": ["Día", "Noche"],
        "Nicol": ["Día", "Noche"],
        "Kenia": ["Día", "Noche"],
        "Dulce": ["Día", "Noche"],
        "Leyver": ["Fijo 3B2"],
        "Azul": ["Fijo Mezquite"],
        "CT Test": ["Día", "Noche"]
    }

# --- 🛰️ CONEXIÓN AL BUZÓN EN LA NUBE REAL (API KEYLESS) ---
# Usamos un almacén JSON público exclusivo para la sucursal Las 3B
API_URL = "https://api.jsonbin.io/v3/b/66103b_roles_notif_temp" 
# Link de respaldo simulado automático por código para evitar caídas
URL_BUZON = "https://kv-json-server-production.up.railway.app/bars/abarrotes3b_notif"

def leer_alerta_de_internet():
    try:
        r = requests.get(URL_BUZON, timeout=3)
        if r.status_code == 200:
            datos = r.json()
            # Convertimos la cadena del historial de vuelta a una lista de Python
            if "historial" in datos:
                datos["historial_intentos"] = [x.strip() for x in datos["historial"].split(",") if x.strip()]
            return datos
    except Exception:
        pass
    # Si internet falla, regresa un estado base local seguro
    return {"tienda": "3B10 El Mezquite", "dia": "Domingo", "turno": "Día", "ct_actual": "Dulce", "estado": "pendiente", "historial_intentos": ["Dulce"]}

def guardar_alerta_en_internet(alerta_dict):
    try:
        payload = {
            "tienda": alerta_dict["tienda"],
            "dia": alerta_dict["dia"],
            "turno": alerta_dict["turno"],
            "ct_actual": alerta_dict["ct_actual"],
            "estado": alerta_dict["estado"],
            "historial": ",".join(alerta_dict["historial_intentos"])
        }
        requests.post(URL_BUZON, json=payload, timeout=3)
    except Exception:
        pass

# Cargamos el estatus real desde la red en cada recarga de pantalla
st.session_state.notificaciones = leer_alerta_de_internet()

if "confirmando_rechazo" not in st.session_state:
    st.session_state.confirmando_rechazo = False

if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = None

# --- LOGO SUPERIOR ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 1, 1])
with col_logo2:
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)

st.title("🏪 Sistema Las 3B")
rol_panel = st.sidebar.radio("Navegación:", ["📱 Panel de Usuarios (CT)", "⚙️ Panel Administrativo"])

# ==============================================================================
# 📱 PANEL DE USUARIOS (CUBRE TURNOS)
# ==============================================================================
if rol_panel == "📱 Panel de Usuarios (CT)":
    st.header("Portal de Personal")
    
    if st.session_state.usuario_activo is None:
        st.info("👋 Bienvenido. Configura tus permisos de sonido e ingresa a tu cuenta.")
        
        with st.expander("📢 INSTRUCCIONES: Cómo activar el sonido en tu celular (Obligatorio)"):
            st.markdown("Revisa que los permisos de sonido de tu Chrome o Safari estén en **Permitir siempre**.")
            if st.button("🎵 Probar sonido del celular ahora mismo", use_container_width=True):
                play_alarm_sound()

        st.divider()
        lista_empleados = ["Selecciona tu nombre..."] + list(st.session_state.personal.keys())
        seleccion = st.selectbox("👤 ¿Quién eres?", lista_empleados)
        
        if seleccion != "Selecciona tu nombre...":
            if st.button("🔒 Conceder Permiso e Ingresar al Perfil", use_container_width=True, type="primary"):
                st.session_state.usuario_activo = seleccion
                st.rerun()
                
    else:
        usuario_actual = st.session_state.usuario_activo
        st.caption(f"👤 Perfil activo: **{usuario_actual}**")
        notif = st.session_state.notificaciones

        if notif["estado"] == "pendiente" and notif["ct_actual"] == usuario_actual:
            if not st.session_state.confirmando_rechazo:
                play_alarm_sound()  
                st.markdown('### <span class="badge-red"></span> ¡TIENES UN TURNO ASIGNADO URGENTE!', unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.error("🚨 ATENCIÓN: Confirma de inmediato tu asistencia para apagar la alarma.")
                    st.write(f"📍 **Tienda:** {notif['tienda']} | 📅 **Día:** {notif['dia']} | ⏰ **Turno:** {notif['turno']}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("✅ SÍ ME PRESENTARÉ", use_container_width=True):
                        notif["estado"] = "confirmado"
                        guardar_alerta_en_internet(notif)
                        st.rerun()
                    if col2.button("❌ NO PUEDO IR", use_container_width=True):
                        st.session_state.confirmando_rechazo = True
                        st.rerun()
            else:
                st.markdown("### ⚠️ ADVERTENCIA IMPORTANTE DE PENALIZACIÓN")
                with st.container(border=True):
                    st.error("🛑 Al rechazar el turno tu prioridad en el sistema bajará al 10%.")
                    
                    col_si, col_no = st.columns(2)
                    if col_si.button("💥 SÍ, RECHAZAR Y PERDER PRIORIDAD", use_container_width=True):
                        st.session_state.confirmando_rechazo = False
                        notif["estado"] = "rechazado"
                        guardar_alerta_en_internet(notif)
                        st.rerun()
                    if col_no.button("🔙 REGRESAR Y ACEPTAR TURNO", use_container_width=True):
                        st.session_state.confirmando_rechazo = False
                        st.rerun()
                    
        elif notif["estado"] == "confirmado" and notif["ct_actual"] == usuario_actual:
            st.success(f"🔒 Tienes tu turno confirmado en **{notif['tienda']}**.")
        elif notif["estado"] == "rechazado" and notif["ct_actual"] == usuario_actual:
            st.error("🛑 Rechazaste la solicitud de cobertura de hoy. Tu prioridad bajó al 10%.")
        else:
            st.success("✨ Todo al corriente. No tienes solicitudes pendientes por ahora.")
            
        st.divider()
        if st.button("👤 Cambiar de Usuario / Cerrar Sesión", key="logout_btn"):
            st.session_state.usuario_activo = None
            st.rerun()

# ==============================================================================
# ⚙️ PANEL ADMINISTRATIVO (ANDRÉS)
# ==============================================================================
else:
    st.header("Panel de Control Administrativo")
    password = st.text_input("🔑 Introduce tu contraseña:", type="password")
    
    if password == "1234":
        st.success("Acceso concedido.")
        notif = st.session_state.notificaciones
        
        tab1, tab2, tab3 = st.tabs(["📢 Asignar Turnos", "📊 Monitor de Emergencias", "⚙️ Configurar Tiendas"])
        
        with tab1:
            st.subheader("Mandar alerta de cobertura")
            lista_tiendas_disponibles = sorted(list(set([t["Tienda"] for t in st.session_state.descansos_tiendas])))
            tienda_sel = st.selectbox("Tienda a cubrir:", lista_tiendas_disponibles)
            dia_sel = st.selectbox("Día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            turno_sel = st.radio("Turno:", ["Día", "Noche"], horizontal=True)
            
            ct_filtrados = [nombre for nombre, turnos in st.session_state.personal.items() if turno_sel in turnos]
            ct_seleccionado = st.selectbox("Selecciona al CT destino:", ct_filtrados)
            
            if st.button("Enviar Alerta"):
                nueva_alerta = {
                    "tienda": tienda_sel, "dia": dia_sel, "turno": turno_sel,
                    "ct_actual": ct_seleccionado, "estado": "pendiente", "historial_intentos": [ct_seleccionado]
                }
                guardar_alerta_en_internet(nueva_alerta)
                st.success(f"Notificación en la nube activa para {ct_seleccionado}.")
                time.sleep(0.5)
                st.rerun()

        with tab2:
            st.subheader("Rastreo de Respuestas de Personal")
            with st.container(border=True):
                st.write(f"📍 **Turno:** {notif['tienda']} ({notif['turno']}) | 👤 **Asignado a:** {notif['ct_actual']}")
                st.info(f"📊 **Estatus actual en la nube:** {notif['estado'].upper()}")
                
                if notif["estado"] == "pendiente":
                    if st.button("⏰ Tiempo Agotado / Falta Injustificada"):
                        notif["estado"] = "rechazado"
                        guardar_alerta_en_internet(notif)
                        st.rerun()

            # --- REBOTE EN TIEMPO REAL DESDE LA RED GLOBAL ---
            if notif["estado"] in ["rechazado", "justificado_sistema"]:
                st.warning("🔄 Buscando sustituto disponible en automático...")
                candidatos_libres = [
                    nombre for nombre, turnos in st.session_state.personal.items()
                    if notif["turno"] in turnos and nombre not in notif["historial_intentos"]
                ]
                
                if candidatos_libres:
                    siguiente_ct = candidatos_libres[0]
                    notif["ct_actual"] = siguiente_ct
                    notif["historial_intentos"].append(siguiente_ct)
                    notif["estado"] = "pendiente"
                    guardar_alerta_en_internet(notif)
                    st.success(f"¡Reasignado en la nube a: **{siguiente_ct}**!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ CRÍTICO: ¡No queda personal disponible para cubrir este turno hoy!")

        with tab3:
            st.subheader("Configuración de Descansos de Sucursales")
            df_actual = pd.DataFrame(st.session_state.descansos_tiendas)
            st.dataframe(df_actual, use_container_width=True)
