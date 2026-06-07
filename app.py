import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE ESTILOS (PUNTO ROJO PARPADEANTE) ---
st.markdown("""
    <style>
    .badge-red { 
        height: 18px; width: 18px; background-color: #ff4b4b; 
        border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; 
    }
    @keyframes pulse { 
        0% { transform: scale(0.9); opacity: 1; } 
        70% { transform: scale(1.2); opacity: 0.7; } 
        100% { transform: scale(0.9); opacity: 1; } 
    }
    </style>
    """, unsafe_allow_html=True)

def play_voice_alert():
    audio_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 1. INICIALIZACIÓN DE BASES DE DATOS EN MEMORIA ---
# Guardamos los descansos de las tiendas en st.session_state para que puedas modificarlos en vivo
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
        "Leyver": ["Fijo 3B2"],
        "Azul": ["Fijo Mezquite"]
    }

if "notificaciones" not in st.session_state:
    st.session_state.notificaciones = {
        "Leyver": {"tienda": "3B2 Pueblo Nuevo", "dia": "Domingo", "turno": "Día", "estado": "pendiente"},
        "Azul": {"tienda": "3B10 El Mezquite", "dia": "Sábado/Domingo", "turno": "Día", "estado": "pendiente"}
    }

# --- 2. MENÚ LATERAL ---
st.title("🏪 Sistema Las 3B - Control de Turnos")
rol_panel = st.sidebar.radio("Ir al Panel:", ["📱 Panel de Usuarios (CT)", "⚙️ Panel Administrativo"])

# ==============================================================================
# 📱 PANEL DE USUARIOS (CUBRE TURNOS)
# ==============================================================================
if rol_panel == "📱 Panel de Usuarios (CT)":
    st.header("Portal de Personal")
    
    lista_empleados = ["Selecciona tu nombre..."] + list(st.session_state.personal.keys())
    usuario_actual = st.selectbox("👤 Identifícate para ingresar:", lista_empleados)

    if usuario_actual != "Selecciona tu nombre...":
        st.divider()
        notif = st.session_state.notificaciones.get(usuario_actual)

        if notif and notif["estado"] == "pendiente":
            play_voice_alert()
            st.markdown('### <span class="badge-red"></span> ¡TIENES UN TURNO ASIGNADO!', unsafe_allow_html=True)
            
            with st.container(border=True):
                st.warning(f"Hola **{usuario_actual}**, confirma tu asistencia:")
                st.write(f"📍 **Tienda:** {notif['tienda']}")
                st.write(f"📅 **Día:** {notif['dia']}")
                st.write(f"⏰ **Turno:** {notif['turno']}")
                
                col1, col2 = st.columns(2)
                if col1.button("✅ CONFIRMAR", use_container_width=True):
                    st.session_state.notificaciones[usuario_actual]["estado"] = "confirmado"
                    st.success("¡Gracias! Turno confirmado.")
                    st.balloons()
                    st.rerun()
                if col2.button("❌ RECHAZAR", use_container_width=True):
                    st.session_state.notificaciones[usuario_actual]["estado"] = "rechazado"
                    st.error("Turno rechazado. Avisando a administración...")
                    st.rerun()
                    
        elif notif and notif["estado"] == "confirmado":
            st.success(f"🔒 Tienes tu turno confirmado en **{notif['tienda']}**.")
        else:
            st.success("✨ No tienes solicitudes pendientes por responder.")

# ==============================================================================
# ⚙️ PANEL ADMINISTRATIVO (ANDRÉS)
# ==============================================================================
else:
    st.header("Panel de Control Administrativo")
    password = st.text_input("🔑 Introduce la contraseña de Administrador:", type="password")
    
    if password == "1234":
        st.success("Acceso concedido.")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Agregar Nuevo CT", 
            "📢 Asignar Turnos", 
            "📊 Ver Confirmaciones",
            "⚙️ Configurar Tiendas"  # Nueva Pestaña
        ])
        
        # TAB 1: REGISTRAR NUEVOS COLABORADORES
        with tab1:
            st.subheader("Registrar nuevo Cubre Turnos")
            with st.form("nuevo_ct_form", clear_on_submit=True):
                nuevo_nombre = st.text_input("Nombre del nuevo CT:")
                st.write("Selecciona los turnos en los que tiene disponibilidad:")
                disp_dia = st.checkbox("Turno Día")
                disp_noche = st.checkbox("Turno Noche")
                disp_domingo = st.checkbox("Solo Domingo Día")
                
                boton_guardar = st.form_submit_button("Guardar en el Sistema")
                
                if boton_guardar and nuevo_nombre:
                    turnos_lista = []
                    if disp_dia: turnos_lista.append("Día")
                    if disp_noche: turnos_lista.append("Noche")
                    if disp_domingo: turnos_lista.append("Domingo Día")
                    
                    if not turnos_lista:
                        st.error("Debes seleccionar al menos una disponibilidad de turno.")
                    else:
                        st.session_state.personal[nuevo_nombre] = turnos_lista
                        st.success(f"¡{nuevo_nombre} ha sido agregado exitosamente!")
                        st.rerun()

        # TAB 2: ENVIAR SOLICITUDES
        with tab2:
            st.subheader("Mandar alerta de cobertura")
            
            # Obtener la lista de tiendas directamente desde la configuración actual
            lista_tiendas_disponibles = sorted(list(set([t["Tienda"] for t in st.session_state.descansos_tiendas])))
            
            tienda_sel = st.selectbox("Tienda a cubrir:", lista_tiendas_disponibles)
            dia_sel = st.selectbox("Día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            turno_sel = st.radio("Turno a cubrir:", ["Día", "Noche"], horizontal=True)
            
            ct_filtrados = [nombre for nombre, turnos in st.session_state.personal.items() if turno_sel in turnos]
            ct_seleccionado = st.selectbox("Selecciona qué CT recibirá la notificación:", ct_filtrados)
            
            if st.button("Enviar Punto Rojo y Audio"):
                st.session_state.notificaciones[ct_seleccionado] = {
                    "tienda": tienda_sel,
                    "dia": dia_sel,
                    "turno": turno_sel,
                    "estado": "pendiente"
                }
                st.success(f"Notificación enviada a {ct_seleccionado}.")

        # TAB 3: VER CONFIRMACIONES
        with tab3:
            st.subheader("Estatus del Rol de la Semana")
            if st.session_state.notificaciones:
                st.json(st.session_state.notificaciones)
            else:
                st.write("No se han enviado asignaciones esta semana.")
                
        # TAB 4: MODIFICAR DESCANSOS DE LAS TIENDAS
        with tab4:
            st.subheader("Modificar Días de Descanso de las Sucursales")
            st.write("Selecciona una tienda y el turno para cambiar su día de descanso asignado:")
            
            # Crear una tabla visual para ver cómo están actualmente antes de cambiar
            df_actual = pd.DataFrame(st.session_state.descansos_tiendas)
            st.dataframe(df_actual, use_container_width=True)
            
            st.divider()
            
            # Formulario de modificación
            tienda_a_modificar = st.selectbox("1. Selecciona la Tienda:", sorted(list(set(df_actual["Tienda"]))))
            turno_a_modificar = st.radio("2. Selecciona el Turno:", ["Día", "Noche"], horizontal=True)
            nuevo_dia_descanso = st.selectbox("3. Selecciona el Nuevo Día de Descanso:", 
                                              ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo", "Ninguno"])
            
            if st.button("🔄 Actualizar Descanso"):
                encontrado = False
                # Buscar en la lista y actualizar el día
                for item in st.session_state.descansos_tiendas:
                    if item["Tienda"] == tienda_a_modificar and item["Turno"] == turno_a_modificar:
                        item["Día Descanso"] = nuevo_dia_descanso
                        encontrado = True
                
                # Caso especial: Si una tienda no tenía descanso en ese turno y ahora sí, o viceversa
                if not encontrado:
                    st.session_state.descansos_tiendas.append({
                        "Tienda": tienda_a_modificar,
                        "Turno": turno_a_modificar,
                        "Día Descanso": nuevo_dia_descanso
                    })
                
                st.success(f"¡Cambio guardado! Ahora **{tienda_a_modificar}** ({turno_a_modificar}) descansa los **{nuevo_dia_descanso}**.")
                st.rerun()
                
    elif password != "":
        st.error("Contraseña incorrecta.")
