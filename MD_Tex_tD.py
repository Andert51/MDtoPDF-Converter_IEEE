import pypandoc
import os
import subprocess
import re  # <--- [NUEVO] Necesario para traducir la sintaxis de las imágenes


def ejecutar_pipeline(input_md):
    base = os.path.splitext(input_md)[0]
    output_tex = f"{base}.tex"
    output_pdf = f"{base}.pdf"
    output_docx = f"{base}.docx"
    temp_md = f"{base}_temp.md"  # <--- [NUEVO] Archivo de trabajo temporal

    # --- MAGIA DE PRE-PROCESAMIENTO PARA IMÁGENES ---
    print(f"[*] Pre-procesando sintaxis de imágenes para: {input_md}")
    with open(input_md, 'r', encoding='utf-8') as f:
        md_data = f.read()

    # Traduce ![[imagen.png]] o ![[imagen.png|Pie de foto]] a ![Pie de foto](imagen.png)
    md_data = re.sub(
        r'!\[\[([^|\]]+)(?:\|([^\]]+))?\]\]',
        lambda m: f"![{m.group(2) or ''}]({m.group(1)})",
        md_data
    )

    # Guardar el contenido corregido en el archivo temporal
    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(md_data)

    args_pdf = [
        '--template=tD_Template.tex',
        '--pdf-engine=lualatex',
        '-V', 'lang=es-ES',
        '--columns=10'  # <--- SECRETO 1: Obliga a Pandoc a ajustar SIEMPRE el ancho de las tablas
    ]

    try:
        print(f"[*] Iniciando producción documental...")

        # Generación de DOCX (Usando el archivo temporal)
        pypandoc.convert_file(temp_md, 'docx', outputfile=output_docx)

        # Traducción a LaTeX (Usando el archivo temporal)
        pypandoc.convert_file(temp_md, 'latex', outputfile=output_tex, extra_args=args_pdf)

        # Post-Procesamiento
        with open(output_tex, 'r', encoding='utf-8') as f:
            tex_data = f.read()

        # Ajuste para bloques de código
        tex_data = tex_data.replace(r'\begin{Shaded}', r'\begin{Shaded}\small')
        tex_data = tex_data.replace(r'\begin{verbatim}', r'\begin{verbatim}\small')

        # --- MAGIA ANTI-SOLAPAMIENTO PARA TABLAS ---
        tex_data = tex_data.replace(r'\raggedright', r'\RaggedRight')
        tex_data = tex_data.replace(r'\_', r'\_\allowbreak ')

        with open(output_tex, 'w', encoding='utf-8') as f:
            f.write(tex_data)

        # Compilación PDF con LuaLatex
        print(f"[*] Compilando PDF final con LuaLaTeX...")
        subprocess.run(['lualatex', '--interaction=nonstopmode', output_tex],
                       capture_output=True, text=True, encoding='utf-8')

        # Limpieza selectiva (incluyendo el archivo temporal)
        archivos_basura = ['.log', '.aux', '.out', '.fls', '.fdb_latexmk', '.synctex.gz']
        for ext in archivos_basura:
            if os.path.exists(f"{base}{ext}"):
                os.remove(f"{base}{ext}")

        # Eliminar el markdown temporal
        if os.path.exists(temp_md):
            os.remove(temp_md)

        print(f"\n=> Producción completada exitosamente:")
        print(f"   - PDF: {output_pdf}")
        print(f"   - DOCX: {output_docx}")
        print(f"   - TEX: {output_tex}")

    except Exception as e:
        print(f"\n[!] Error en la cadena de producción: {e}")


if __name__ == "__main__":
    nombre_archivo = "Reporte_IMRAD_DAC_DDS.md"
    if os.path.exists(nombre_archivo):
        ejecutar_pipeline(nombre_archivo)
    else:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")