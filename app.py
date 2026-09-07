import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="V°B° Películas Plásticas", layout="wide")

# CSS personalizado para la interfaz gráfica
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #1F4E78;
    }
    
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #1F4E78 !important;
    }

    div[data-baseweb="checkbox"] span:first-child {
        border-color: #1F4E78 !important;
    }
    
    div[data-baseweb="checkbox"] [aria-checked="true"] {
        background-color: #28A745 !important;
        border-color: #28A745 !important;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #F8F9FA !important;
        color: #1F4E78 !important;
        border: 1px solid #1F4E78 !important;
    }

    .paro-box {
        background-color: #E8F4F8;
        border-left: 5px solid #1F4E78;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Clase FPDF optimizada para evitar caracteres Unicode no soportados
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(31, 78, 120)
        self.cell(0, 8, 'HOJA DE INSTRUCCIONES Y RESUMEN DE V°B°', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 6, 'Documento Oficial de Control para el Operador de Impresion', 0, 1, 'C')
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generar_pdf_completo(reg):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    def agregar_seccion(titulo):
        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(31, 78, 120)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 6, f"  {titulo.upper()}", 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(1)

    def agregar_campo(lbl, val, width=65):
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(31, 78, 120)
        pdf.cell(width, 5, f"{lbl}:", 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, str(val), 0, 1)

    # 1. Datos Generales
    agregar_seccion("1. DATOS GENERALES DEL TRABAJO")
    agregar_campo("Fecha y Hora de Registro", reg.get("Hora Registro", ""))
    agregar_campo("Trabajo / Producto", reg.get("Trabajo", ""))
    agregar_campo("Codigo de Producto", reg.get("Codigo", ""))
    agregar_campo("Fecha de Produccion", reg.get("Fecha", ""))
    agregar_campo("Supervisor a Cargo", reg.get("Supervisor", ""))
    agregar_campo("Operador de Maquina", reg.get("Operador", ""))
    agregar_campo("Velocidad de Operacion", f"{reg.get('Velocidad', '')} m/min")
    agregar_campo("Delta Maximo General (Delta E)", reg.get("Delta Maximo General", ""))
    agregar_campo("Calificacion de Arranque", reg.get("Calificacion Arranque", ""))
    pdf.ln(2)

    # 2. Resumen Completo de Evaluaciones
    agregar_seccion("2. EVALUACION DETALLADA POR SECCION")
    for sec in ["FONDO", "IMAGEN", "TEXTOS"]:
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(31, 78, 120)
        pdf.cell(0, 5, f"> EVALUACION EN {sec}:", 0, 1)
        
        agregar_campo("  * Dictamen / Resultado", reg.get(f"Res_{sec}", ""))
        agregar_campo("  * Delta Maximo Medido", reg.get(f"Delta_{sec}", ""))
        agregar_campo("  * Criterio de Prioridad", reg.get(f"Prio_{sec}", ""))
        agregar_campo("  * Elementos de Referencia", reg.get(f"Ref_{sec}", "Ninguno"))
        agregar_campo("  * Observaciones y Notas", reg.get(f"Notas_{sec}", "Sin comentarios"))
        pdf.ln(1)

    # 3. Herramental y Paro
    agregar_seccion("3. CONTROL DE HERRAMENTAL Y CRITERIO DE PARO")
    agregar_campo("Estado de Placa", reg.get("Estado Placa", ""))
    agregar_campo("Estado de Rasqueta", reg.get("Estado Rasqueta", ""))
    agregar_campo("Cambio Programado de Placas", f"{reg.get('Cambiar Placas', '')} {reg.get('Unidad Placa', '')}")
    agregar_campo("Cambio Programado de Rasquetas", f"{reg.get('Cambiar Rasquetas', '')} {reg.get('Unidad Rasqueta', '')}")
    
    pdf.set_font('Arial', 'B', 9)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 5, "LIMITES DE PARO DE MAQUINA PARA EL OPERADOR:", 0, 1)
    agregar_campo("  * Limite por Volumen (Hits)", reg.get("Limite Paro (Hits)", ""))
    agregar_campo("  * Limite por Tiempo (Minutos)", reg.get("Limite Paro (Min)", ""))
    agregar_campo("  * Accion Obligatoria al Cumplir Limite", reg.get("Accion Paro", ""))
    pdf.ln(2)

    # 4. Autorizaciones
    agregar_seccion("4. FIRMAS Y AUTORIZACIONES")
    roles = ["Gerente Preprensa", "Coordinador Impresion", "Gerente Produccion", "Coordinador Calidad", "Supervisor de Turno"]
    for role in roles:
        agregar_campo(role, reg.get(role, ""))

    # Retorno de bytes compatible con fpdf/fpdf2
    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return str(out).encode('latin-1', 'replace')

# Inicializar sesión
if "registros" not in st.session_state:
    st.session_state.registros = []

st.title("📋 Lista de V°B° - Películas Plásticas")
st.caption("Guía y Registro de Evaluación de Impresión Online")

tab_captura, tab_registros = st.tabs(["📝 Llenar Formulario", "📊 Ver Registros Guardados y Descargar PDF"])

with tab_captura:
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

    def render_eval_section(title, prefix):
        st.subheader(f"Evaluación: {title}")
        c1, c2, c3, c4 = st.columns(4)
        
        refs_seleccionadas = []
        with c1:
            st.markdown("**Soporte / Presentación**")
            if st.checkbox("Carta Laminada", key=f"{prefix}_carta"): refs_seleccionadas.append("Carta Laminada")
            if st.checkbox("Sin Laminar", key=f"{prefix}_sin_lam"): refs_seleccionadas.append("Sin Laminar")
            
        with c2:
            st.markdown("**Elementos de Referencia**")
            if st.checkbox("Pantone Digital", key=f"{prefix}_p_dig"): refs_seleccionadas.append("Pantone Digital")
            if st.checkbox("Pantone Físico", key=f"{prefix}_p_fis"): refs_seleccionadas.append("Pantone Físico")
            if st.checkbox("Muestra Cliente", key=f"{prefix}_m_cli"): refs_seleccionadas.append("Muestra Cliente")
            if st.checkbox("Prueba de Color", key=f"{prefix}_p_col"): refs_seleccionadas.append("Prueba de Color")
            
        with c3:
            st.markdown("**Criterio y Mediciones**")
            if st.checkbox("Color Cert", key=f"{prefix}_c_cert"): refs_seleccionadas.append("Color Cert")
            delta = st.number_input("Delta Máx", min_value=0.0, value=1.5, step=0.1, key=f"{prefix}_delta")
            prioridad = st.radio("Prioridad", ["Apariencia", "Medición"], horizontal=True, key=f"{prefix}_prio")

        with c4:
            st.markdown("**Dictamen**")
            resultado = st.selectbox("Resultado", ["ACEPTABLE", "AJUSTABLE", "RECHAZADO"], key=f"{prefix}_res")
            notas = st.text_area("Notas / Observaciones", height=68, key=f"{prefix}_notas")

        return {
            f"Res_{title}": resultado,
            f"Delta_{title}": delta,
            f"Prio_{title}": prioridad,
            f"Notas_{title}": notas if notas else "Sin observaciones",
            f"Ref_{title}": ", ".join(refs_seleccionadas) if refs_seleccionadas else "Ninguna"
        }

    res_fondo = render_eval_section("FONDO", "f")
    st.divider()
    res_imagen = render_eval_section("IMAGEN", "img")
    st.divider()
    res_textos = render_eval_section("TEXTOS", "txt")
    st.divider()

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

    st.markdown('<div class="paro-box"><b>🛑 CRITERIO DE PARO DE MÁQUINA:</b> Establece los límites máximos para bajar el trabajo sin V°B°.</div>', unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        hits_limite = st.number_input("Bajar trabajo después de (Hits):", min_value=0, value=0, step=500)
    with col_p2:
        minutos_limite = st.number_input("O después de (Minutos sin V°B°):", min_value=0, value=0, step=5)
    with col_p3:
        accion_paro = st.selectbox("Acción al cumplir límite:", ["BAJAR TRABAJO", "NOTIFICAR SUPERVISOR", "ESPERAR AUTORIZACIÓN EXCEPCIONAL"])

    st.divider()

    st.header("5. Responsables y Autorización de V°B°")
    roles = ["Gerente Preprensa", "Coordinador Impresión", "Gerente Producción", "Coordinador Calidad", "Supervisor de Turno"]

    auth_data = {}
    for role in roles:
        r1, r2 = st.columns([2, 2])
        with r1:
            nombre = st.text_input(f"Nombre ({role})", key=f"n_{role}")
        with r2:
            estatus = st.selectbox(f"Estatus ({role})", ["PENDIENTE", "AUTORIZADO", "RECHAZADO", "CON EXCEPCIÓN"], key=f"s_{role}")
        auth_data[role] = f"{nombre} ({estatus})" if nombre else f"Sin Asignar ({estatus})"

    if st.button("💾 Guardar Registro de V°B°", type="primary"):
        nuevo_registro = {
            "Hora Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Trabajo": trabajo,
            "Codigo": codigo,
            "Fecha": str(fecha),
            "Supervisor": supervisor,
            "Operador": operador,
            "Velocidad": velocidad,
            "Delta Maximo General": delta_max,
            "Calificacion Arranque": calificacion,
            **res_fondo,
            **res_imagen,
            **res_textos,
            "Estado Placa": est_placa,
            "Estado Rasqueta": est_rasqueta,
            "Cambiar Placas": cambio_placa,
            "Unidad Placa": u_placa,
            "Cambiar Rasquetas": cambio_rasqueta,
            "Unidad Rasqueta": u_rasqueta,
            "Limite Paro (Hits)": hits_limite,
            "Limite Paro (Min)": minutos_limite,
            "Accion Paro": accion_paro,
            **auth_data
        }
        st.session_state.registros.append(nuevo_registro)
        st.success("¡Registro guardado exitosamente!")

with tab_registros:
    st.header("📊 Histórico de Registros y Descarga de PDF para Operador")
    if len(st.session_state.registros) > 0:
        for idx, reg in enumerate(st.session_state.registros):
            with st.expander(f"📌 Registro #{idx+1} - {reg.get('Trabajo', 'Sin Título')} ({reg.get('Hora Registro', '')})", expanded=(idx==len(st.session_state.registros)-1)):
                c_pdf, c_info = st.columns([1, 3])
                
                with c_pdf:
                    try:
                        pdf_bytes = generar_pdf_completo(reg)
                        st.download_button(
                            label="📄 Descargar PDF para Operador",
                            data=pdf_bytes,
                            file_name=f"VOB_OPERADOR_{reg.get('Trabajo','Producto')}_{idx+1}.pdf",
                            mime="application/pdf",
                            key=f"btn_pdf_{idx}"
                        )
                    except Exception as e:
                        st.error(f"Error al generar PDF: {e}")

                with c_info:
                    st.markdown(f"**Código:** {reg.get('Codigo')} | **Operador:** {reg.get('Operador')} | **Supervisor:** {reg.get('Supervisor')}")
                    st.markdown(f"**Resultados:** Fondo: `{reg.get('Res_FONDO')}` | Imagen: `{reg.get('Res_IMAGEN')}` | Textos: `{reg.get('Res_TEXTOS')}`")
                    st.markdown(f"**Criterio de Paro:** {reg.get('Limite Paro (Hits)')} Hits / {reg.get('Limite Paro (Min)')} Minutos -> *{reg.get('Accion Paro')}*")

        st.divider()
        df = pd.DataFrame(st.session_state.registros)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar todos los registros a Excel (CSV)",
            data=csv,
            file_name=f"registros_vobo_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aún no hay registros guardados en esta sesión. Llena el formulario y presiona 'Guardar Registro'.")
