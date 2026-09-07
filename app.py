import streamlit as st

st.set_page_config(page_title="V°B° Películas Plásticas", layout="wide")

st.title("📋 Lista de V°B° - Películas Plásticas")
st.caption("Guía y Registro de Evaluación de Impresión Online")

# DATOS GENERALES
st.header("1. Datos Generales del Trabajo")
col1, col2, col3, col4 = st.columns(4)
with col1:
    trabajo = st.text_input("Trabajo / Producto")
    fecha = st.date_input("Fecha")
with col2:
    codigo = st.text_input("Código")
    velocidad = st.number_input("Velocidad (m/min)", min_value=0)
with col3:
    supervisor = st.text_input("Supervisor")
    delta_max = st.number_input("Delta Máximo (ΔE)", min_value=0.0, value=2.0)
with col4:
    operador = st.text_input("Operador")
    calificacion = st.selectbox("Calificación Arranque", ["Aceptable", "Ajustable", "Rechazado"])

st.divider()

# EVALUACIONES (FONDO, IMAGEN, TEXTOS)
def render_eval(title):
    st.subheader(f"Evaluación: {title}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**Soporte**")
        st.checkbox(f"Carta Laminada ({title})")
        st.checkbox(f"Sin Laminar ({title})")
    with c2:
        st.markdown("**Referencias**")
        st.checkbox(f"Pantone Digital ({title})")
        st.checkbox(f"Pantone Físico ({title})")
        st.checkbox(f"Muestra Cliente ({title})")
        st.checkbox(f"Prueba Color ({title})")
    with c3:
        st.markdown("**Medición**")
        st.checkbox(f"Color Cert ({title})")
        st.number_input(f"Delta Máx ({title})", min_value=0.0, value=1.5)
        st.radio(f"Prioridad ({title})", ["Apariencia", "Medición"], horizontal=True)
    with c4:
        st.markdown("**Dictamen**")
        st.selectbox(f"Resultado ({title})", ["ACEPTABLE", "AJUSTABLE", "RECHAZADO"])
        st.text_area(f"Notas ({title})", height=68)

render_eval("1. FONDO")
render_eval("2. IMAGEN")
render_eval("3. TEXTOS")

st.divider()

# HERRAMENTAL
st.header("4. Estado de Herramental")
ch1, ch2, ch3 = st.columns(3)
with ch1:
    st.selectbox("Estado Placa", ["NUEVA", "VIDA ÚTIL OK", "CAMBIAR"])
    st.selectbox("Estado Rasqueta", ["NUEVA", "VIDA ÚTIL OK", "CAMBIAR"])
with ch2:
    st.number_input("Cambiar Placas después de", min_value=0)
    st.number_input("Cambiar Rasquetas después de", min_value=0)
with ch3:
    st.selectbox("Unidad Placa", ["HITS", "MINUTOS"])
    st.selectbox("Unidad Rasqueta", ["HITS", "MINUTOS"])

st.divider()

# AUTORIZACIONES
st.header("5. Autorización y Responsables")
roles = ["Gerente Preprensa", "Coordinador Impresión", "Gerente Producción", "Coordinador Calidad", "Supervisor Turno"]
for role in roles:
    r1, r2 = st.columns(2)
    r1.text_input(f"Responsable: {role}")
    r2.selectbox(f"Estatus: {role}", ["PENDIENTE", "AUTORIZADO", "RECHAZADO", "EXCEPCIÓN"])

if st.button("💾 Guardar Registro de V°B° Online", type="primary"):
    st.success("¡Registro guardado correctamente!")
