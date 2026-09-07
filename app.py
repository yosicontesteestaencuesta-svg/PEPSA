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

    # Retorno compatible con bytearray, bytes o str
    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return str(out).encode('latin-1', 'replace')
