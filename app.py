import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="V°B° Películas Plásticas", layout="wide")

# Inicializar almacenamiento en memoria si no existe
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
            carta = st.checkbox(f"Carta Laminada", key=f"{prefix}_carta")
            sin_lam = st.checkbox(f"Sin Laminar", key=f"{prefix}_sin_lam")
            
        with c2:
            st.markdown("**Elementos de Referencia**")
            p_dig = st.checkbox(f"Pantone Digital", key=f"{prefix}_p_dig")
            p_fis = st.checkbox(f"Pantone Físico", key=f"{prefix}_p_fis")
            m_cli = st.checkbox(f"Muestra Cliente", key=f"{prefix}_m_cli")
            p_col = st.checkbox(f"Prueba de Color", key=f"{prefix}_p_col")
            
        with c3:
            st.markdown("**Criterio y Mediciones**")
            c_cert = st.checkbox(f"Color Cert", key=f"{prefix}_c_cert")
            delta = st.number_input(f"Delta Máx", min_value=0.0, value=1.5, step=0.1, key=f"{prefix}_delta")
            prioridad = st.radio(f"Prioridad", ["Apariencia", "Medición"], horizontal=True, key=f"{prefix}_prio")

        with c4:
            st.markdown("**Dictamen**")
            resultado = st.selectbox(f"Resultado", ["ACEPTABLE", "AJUSTABLE", "RECHAZADO"], key=f"{prefix}_res")
            notas = st.text_area(f"Notas / Observaciones", height=68, key=f"{prefix}_notas")

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

    # --- SECCIÓN HERRAMENTAL ---
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

    st.error("⚠️ **CRITERIO DE PARO:** Bajar trabajo después de un tiempo o volumen límite sin V°B°.")

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
            **auth_data
        }
        st.session_state.registros.append(nuevo_registro)
        st.success("¡Registro guardado exitosamente!")

with tab_registros:
    st.header("📊 Histórico de Registros de V°B°")
    if len(st.session_state.registros) > 0:
        df = pd.DataFrame(st.session_state.registros)
        
        # Muestra la tabla interactiva
        st.dataframe(df, use_container_width=True)
        
        # Botón para descargar la lista en Excel / CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar todos los registros a Excel (CSV)",
            data=csv,
            file_name=f"registros_vobo_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aún no hay registros guardados en esta sesión. Llena el formulario y presiona 'Guardar Registro'.")
