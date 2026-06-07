import streamlit as st
import pandas as pd
import time

# --- CONFIGURACIÓN DE LA PÁGINA (Para que en celular se vea como App) ---
st.set_page_config(page_title="Las 3B - Roles", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILOS VISUALES (Punto rojo parpadeante de notificación) ---
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
    # Sonido de alarma insistente en bucle para el "despertador" PWA
    audio_html = """
        <audio autoplay loop>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 1. BASES DE DATOS EN MEMORIA (Sesión Activa) ---
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
        "Azul": ["Fijo Mezquite"]
    }

if "notificaciones" not in st.session_state:
    # Simulación de un turno inicial asignado para pruebas
    st.session_state.notificaciones = {
        "tienda": "3B5 Lomas Dos",
        "dia": "Martes",
        "turno": "Noche",
        "historial_intentos": ["Sofía"],
        "ct_actual": "Sofía",
        "estado": "pendiente"
    }

# --- 2. MENÚ LATERAL (Para cambiar de Rol) ---
st.title("🏪 Sistema Las 3B")
rol_panel = st.sidebar.radio("Navegación:", ["📱 Panel de Usuarios (CT)", "⚙️ Panel Administrativo"])

# ==============================================================================
# 📱 PANEL DE USUARIOS (CUBRE TURNOS)
# ==============================================================================
if rol_panel == "📱 Panel de Usuarios (CT)":
    st.header("Portal de Personal")
    
    lista_empleados = ["Selecciona tu nombre..."] + list(st.session_state.personal.keys())
    usuario_actual = st.selectbox("👤 Identifícate para ingresar:", lista_empleados)

    if usuario_actual != "Selecciona tu nombre...":
        st.divider()
        notif = st.session_state.notificaciones

        # Lógica del "Despertador" si el usuario es el asignado actual y está pendiente
        if notif["estado"] == "pendiente" and notif["ct_actual"] == usuario_actual:
            play_alarm_sound()  # Suena en bucle insistente
            st.markdown('### <span class="badge-red"></span> ¡TIENES UN TURNO ASIGNADO URGENTE!', unsafe_allow_html=True)
            
            with st.container(border=True):
                st.error("🚨 ATENCIÓN: Confirma de inmediato tu asistencia para apagar la alarma.")
                st.write(f"📍 **Tienda:** {notif['tienda']}")
                st.write(f"📅 **Día:** {notif['dia']} | ⏰ **Turno:** {notif['turno']}")
                
                col1, col2 = st.columns(2)
                if col1.button("✅ SÍ ME PRESENTARÉ", use_container_width=True):
                    st.session_state.notificaciones["estado"] = "confirmado"
                    st.success("¡Turno confirmado! Alarma desactivada.")
                    st.balloons()
                    st.rerun()
                if col2.button("❌ NO PUEDO IR", use_container_width=True):
                    st.session_state.notificaciones["estado"] = "rechazado"
                    st.rerun()
                    
        elif notif["estado"] == "confirmado" and notif["ct_actual"] == usuario_actual:
            st.success(f"🔒 Tienes tu turno confirmado en **{notif['tienda']}** para el día **{notif['dia']}**.")
        else:
            st.success("✨ Todo al corriente. No tienes solicitudes pendientes por ahora.")

# ==============================================================================
# ⚙️ PANEL ADMINISTRATIVO (ANDRÉS)
# ==============================================================================
else:
    st.header("Panel de Control Administrativo")
    password = st.text_input("🔑 Introduce tu contraseña:", type="password")
    
    if password == "1234":
        st.success("Acceso concedido.")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Agregar Nuevo CT", 
            "📢 Asignar Turnos", 
            "📊 Monitor de Emergencias",
            "⚙️ Configurar Tiendas"
        ])
        
        # TAB 1: REGISTRAR NUEVOS CUBRE TURNOS
        with tab1:
            st.subheader("Registrar nuevo personal")
            with st.form("nuevo_ct_form", clear_on_submit=True):
                nuevo_nombre = st.text_input("Nombre del nuevo CT:")
                st.write("Selecciona su disponibilidad:")
                disp_dia = st.checkbox("Turno Día")
                disp_noche = st.checkbox("Turno Noche")
                disp_domingo = st.checkbox("Solo Domingo Día")
                
                if st.form_submit_button("Guardar en el Sistema") and nuevo_nombre:
                    turnos_lista = []
                    if disp_dia: turnos_lista.append("Día")
                    if disp_noche: turnos_lista.append("Noche")
                    if disp_domingo: turnos_lista.append("Domingo Día")
                    
                    if not turnos_lista:
                        st.error("Selecciona al menos una opción de turno.")
                    else:
                        st.session_state.personal[nuevo_nombre] = turnos_lista
                        st.success(f"¡{nuevo_nombre} integrado al equipo!")
                        st.rerun()

        # TAB 2: ENVIAR SOLICITUDES MANUALES
        with tab2:
            st.subheader("Mandar alerta de cobertura")
            lista_tiendas_disponibles = sorted(list(set([t["Tienda"] for t in st.session_state.descansos_tiendas])))
            tienda_sel = st.selectbox("Tienda a cubrir:", lista_tiendas_disponibles)
            dia_sel = st.selectbox("Día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            turno_sel = st.radio("Turno:", ["Día", "Noche"], horizontal=True)
            
            ct_filtrados = [nombre for nombre, turnos in st.session_state.personal.items() if turno_sel in turnos]
            ct_seleccionado = st.selectbox("Selecciona al CT destino:", ct_filtrados)
            
            if st.button("Enviar Alerta"):
                st.session_state.notificaciones = {
                    "tienda": tienda_sel,
                    "dia": dia_sel,
                    "turno": turno_sel,
                    "historial_intentos": [ct_seleccionado],
                    "ct_actual": ct_seleccionado,
                    "estado": "pendiente"
                }
                st.success(f"Notificación activa para {ct_seleccionado}.")

        # TAB 3: MONITOR DE EMERGENCIAS Y REASIGNACIÓN AUTOMÁTICA
        with tab3:
            st.subheader("Rastreo de Respuestas de Personal")
            notif = st.session_state.notificaciones
            
            with st.container(border=True):
                st.write(f"📍 **Turno Activo:** {notif['tienda']} ({notif['turno']})")
                st.write(f"👤 **Asignado a:** {notif['ct_actual']} | 📊 **Estatus:** {notif['estado'].upper()}")
                
                if notif["estado"] == "pendiente":
                    if st.button("⏰ Simular: Tiempo agotado (No contestó el despertador)"):
                        notif["estado"] = "rechazado"
                        st.rerun()

            # LÓGICA AUTOMÁTICA DE SUSTITUCIÓN
            if notif["estado"] == "rechazado":
                st.warning("🔄 Buscando sustituto desocupado en automático...")
                candidatos_libres = [
                    nombre for nombre, turnos in st.session_state.personal.items()
                    if notif["turno"] in turnos and nombre not in notif["historial_intentos"]
                ]
                
                if candidatos_libres:
                    siguiente_ct = candidatos_libres[0]
                    notif["ct_actual"] = siguiente_ct
                    notif["historial_intentos"].append(siguiente_ct)
                    notif["estado"] = "pendiente"
                    st.success(f"¡Reasignado automáticamente a: **{siguiente_ct}**!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ CRÍTICO: ¡No queda personal disponible para este turno!")

        # TAB 4: MODIFICAR DESCANSOS DE LAS TIENDAS
        with tab4:
            st.subheader("Configuración de Descansos de Sucursales")
            df_actual = pd.DataFrame(st.session_state.descansos_tiendas)
            st.dataframe(df_actual, use_container_width=True)
            
            st.divider()
            tienda_a_modificar = st.selectbox("Selecciona la Tienda:", sorted(list(set(df_actual["Tienda"]))))
            turno_a_modificar = st.radio("Selecciona el Turno:", ["Día", "Noche"], key="mod_turno", horizontal=True)
            nuevo_dia_descanso = st.selectbox("Nuevo Día de Descanso:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo", "Ninguno"])
            
            if st.button("🔄 Actualizar Descanso"):
                encontrado = False
                for item in st.session_state.descansos_tiendas:
                    if item["Tienda"] == tienda_a_modificar and item["Turno"] == turno_a_modificar:
                        item["Día Descanso"] = nuevo_dia_descanso
                        encontrado = True
                if not encontrado:
                    st.session_state.descansos_tiendas.append({"Tienda": fancy_name, "Turno": turno_a_modificar, "Día Descanso": nuevo_dia_descanso})
                st.success("¡Cambio guardado exitosamente!")
                st.rerun()
                
    elif password != "":
        st.error("Contraseña incorrecta.")
