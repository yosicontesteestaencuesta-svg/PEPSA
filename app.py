import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="V°B° Películas Plásticas", layout="wide")

# CSS personalizado para fondo blanco, texto azul marino y casillas seleccionadas en verde
st.markdown("""
    <style>
    /* Fondo principal blanco */
    .stApp {
        background-color: #FFFFFF;
        color: #1F4E78;
    }
    
    /* Textos, títulos y encabezados en Azul Marino */
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #1F4E78 !important;
    }

    /* Estilo para las casillas de verificación (checkboxes) */
    div[data-baseweb="checkbox"] span:first-child {
        border-color: #1F4E78 !important;
    }
    
    /* Pintar de verde la casilla seleccionada */
    div[data-baseweb="checkbox"] [aria-checked="true"] {
        background-color: #28A745 !important;
        border-color: #28A745 !important;
    }

    /* Fondo de inputs y cajas de texto */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #F8F9FA !important;
        color: #1F4E78 !important;
        border: 1px solid #1F4E78 !important;
    }

    /* Estilo del recuadro de Criterio de Paro */
    .paro-box {
        background-color: #E8F4F8;
        border-left: 5px solid #1F4E78;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar almacenamiento en sesión si no existe
if "registros" not in st.session_state:
    st.session_state.registros = []

st.title("📋 Lista de V°B° - Películas Plásticas")
st.caption("Guía y Registro de Evaluación de Impresión Online")

# Pestañas principales
tab_captura, tab_registros = st.tabs(["📝 Llenar Formulario", "📊 Ver Registros Guardados"])

with tab_captura:
    # --- SECCIÓN 1: DATOS GENERALES ---
    st.header("1. Datos Generales del Trabajo")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        trabajo = st.text_input("Trabajo / Producto")
        fecha = st.date_input("Fecha")

    with col2:
        codigo = st.text_input("Código")
        velocidad = st.number_input("Velocidad (m/min)", min_value=0, value=0)

    with col3:
        supervisor = st.text_input("Supervisor")
        delta_max = st.number_input("Delta Máximo (ΔE General)", min_value=0.0, value=2.0, step=0.1)

    with col4:
        operador = st.text_input("Operador")
        calificacion = st.selectbox("Calificación Arranque", ["Aceptable", "Ajustable", "Rechazado"])

    st.divider()

    # --- SECCIÓN EVALUACIONES ---
    def render_eval_section(title, prefix):
        st.subheader(f"Evaluación: {title}")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown("**Soporte / Presentación**")
            carta = st.checkbox("Carta Laminada", key=f"{prefix}_carta")
            sin_lam = st.checkbox("Sin Laminar", key=f"{prefix}_sin_lam")
            
        with c2:
            st.markdown("**Elementos de Referencia**")
            p_dig = st.checkbox("Pantone Digital", key=f"{prefix}_p_dig")
            p_fis = st.checkbox("Pantone Físico", key=f"{prefix}_p_fis")
            m_cli = st.checkbox("Muestra Cliente", key=f"{prefix}_m_cli")
            p_col = st.checkbox("Prueba de Color", key=f"{prefix}_p_col")
            
        with c3:
            st.markdown("**Criterio y Mediciones**")
            c_cert = st.checkbox("Color Cert", key=f"{prefix}_c_cert")
            delta = st.number_input("Delta Máx", min_value=0.0, value=1.5, step=0.1, key=f"{prefix}_delta")
            prioridad = st.radio("Prioridad", ["Apariencia", "Medición"], horizontal=True, key=f"{prefix}_prio")

        with c4:
            st.markdown("**Dictamen**")
            resultado = st.selectbox("Resultado", ["ACEPTABLE", "AJUSTABLE", "RECHAZADO"], key=f"{prefix}_res")
            notas = st.text_area("Notas / Observaciones", height=68, key=f"{prefix}_notas")

        return {
            f"Res_{title}": resultado,
            f"Delta_{title}": delta,
            f"Notas_{title}": notas
        }

    res_fondo = render_eval_section("FONDO", "f")
    st.divider()
    res_imagen = render_eval_section("IMAGEN", "img")
    st.divider()
    res_textos = render_eval_section("TEXTOS", "txt")
    st.divider()

    # --- SECCIÓN HERRAMENTAL Y CRITERIO DE PARO ---
    st.header("4. Estado de Herramental y Cambios")
    col_h1, col_h2, col_h3 = st.columns(3)

    with col_h1:
        est_placa = st.selectbox("Estado de Placa", ["NUEVA", "VIDA ÚTIL OK", "CAMBIAR"])
        est_rasqueta = st.selectbox("Estado de Rasqueta", ["NUEVA", "VIDA ÚTIL OK", "CAMBIAR"])

    with col_h2:
        cambio_placa = st.number_input("Cambiar Placas después de", min_value=0, value=0)
        cambio_rasqueta = st.number_input("Cambiar Rasquetas después de", min_value=0, value=0)

    with col_h3:
        u_placa = st.selectbox("Unidad Placa", ["HITS", "MINUTOS"])
        u_rasqueta = st.selectbox("Unidad Rasqueta", ["HITS", "MINUTOS"])

    # CRITERIO DE PARO PERSONALIZADO
    st.markdown('<div class="paro-box"><b>🛑 CRITERIO DE PARO DE MÁQUINA:</b> Establece los límites máximos para bajar el trabajo sin V°B°.</div>', unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        hits_limite = st.number_input("Bajar trabajo después de (Hits):", min_value=0, value=0, step=500)
    with col_p2:
        minutos_limite = st.number_input("O después de (Minutos sin V°B°):", min_value=0, value=0, step=5)
    with col_p3:
        accion_paro = st.selectbox("Acción al cumplir límite:", ["BAJAR TRABAJO", "NOTIFICAR SUPERVISOR", "ESPERAR AUTORIZACIÓN EXCEPCIONAL"])

    st.divider()

    # --- SECCIÓN AUTORIZACIONES ---
    st.header("5. Responsables y Autorización de V°B°")
    roles = [
        "Gerente Preprensa", "Coordinador Impresión", "Gerente Producción",
        "Coordinador Calidad", "Supervisor de Turno"
    ]

    auth_data = {}
    for role in roles:
        r1, r2 = st.columns([2, 2])
        with r1:
            nombre = st.text_input(f"Nombre ({role})", key=f"n_{role}")
        with r2:
            estatus = st.selectbox(f"Estatus ({role})", ["PENDIENTE", "AUTORIZADO", "RECHAZADO", "CON EXCEPCIÓN"], key=f"s_{role}")
        auth_data[role] = f"{nombre} ({estatus})"

    if st.button("💾 Guardar Registro de V°B°", type="primary"):
        nuevo_registro = {
            "Hora Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Trabajo": trabajo,
            "Código": codigo,
            "Fecha": str(fecha),
            "Supervisor": supervisor,
            "Operador": operador,
            "Velocidad": velocidad,
            "Calificación Arranque": calificacion,
            "Fondo": res_fondo["Res_FONDO"],
            "Imagen": res_imagen["Res_IMAGEN"],
            "Textos": res_textos["Res_TEXTOS"],
            "Estado Placa": est_placa,
            "Estado Rasqueta": est_rasqueta,
            "Límite Paro (Hits)": hits_limite,
            "Límite Paro (Min)": minutos_limite,
            "Acción Paro": accion_paro,
            **auth_data
        }
        st.session_state.registros.append(nuevo_registro)
        st.success("¡Registro guardado exitosamente!")

with tab_registros:
    st.header("📊 Histórico de Registros de V°B°")
    if len(st.session_state.registros) > 0:
        df = pd.DataFrame(st.session_state.registros)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar todos los registros a Excel (CSV)",
            data=csv,
            file_name=f"registros_vobo_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aún no hay registros guardados en esta sesión. Llena el formulario y presiona 'Guardar Registro'.")
