import pypandoc
import os
import subprocess


def ejecutar_pipeline(input_md):
    base = os.path.splitext(input_md)[0]
    output_tex = f"{base}.tex"
    output_pdf = f"{base}.pdf"
    output_docx = f"{base}.docx"

    args_pdf = [
        '--template=tD_Template.tex',
        '--pdf-engine=lualatex',
        '-V', 'lang=es-ES',
        '--columns=10'  # <--- SECRETO 1: Obliga a Pandoc a ajustar SIEMPRE el ancho de las tablas
    ]

    try:
        print(f"[*] Iniciando producción documental para: {input_md}")

        # Generación de DOCX
        pypandoc.convert_file(input_md, 'docx', outputfile=output_docx)

        # Traducción a LaTeX
        pypandoc.convert_file(input_md, 'latex', outputfile=output_tex, extra_args=args_pdf)

        # Post-Procesamiento
        with open(output_tex, 'r', encoding='utf-8') as f:
            tex_data = f.read()

        # Ajuste para bloques de código
        tex_data = tex_data.replace(r'\begin{Shaded}', r'\begin{Shaded}\small')
        tex_data = tex_data.replace(r'\begin{verbatim}', r'\begin{verbatim}\small')

        # --- MAGIA ANTI-SOLAPAMIENTO PARA TABLAS ---
        # 1. Habilitar separación de sílabas en celdas alineadas a la izquierda (requiere ragged2e)
        tex_data = tex_data.replace(r'\raggedright', r'\RaggedRight')

        # 2. Dar permiso a LaTeX para cortar variables de código justo después de un guion bajo
        tex_data = tex_data.replace(r'\_', r'\_\allowbreak ')

        with open(output_tex, 'w', encoding='utf-8') as f:
            f.write(tex_data)

        # Compilación PDF con LuaLatex
        print(f"[*] Compilando PDF final con LuaLaTeX...")
        subprocess.run(['lualatex', '--interaction=nonstopmode', output_tex],
                       capture_output=True, text=True, encoding='utf-8')

        # Limpieza selectiva
        for ext in ['.log', '.aux', '.out', '.fls', '.fdb_latexmk', '.synctex.gz']:
            if os.path.exists(f"{base}{ext}"): os.remove(f"{base}{ext}")

        print(f"\n=> Producción completada exitosamente:")
        print(f"   - PDF: {output_pdf}")
        print(f"   - DOCX: {output_docx}")
        print(f"   - TEX: {output_tex}")

    except Exception as e:
        print(f"\n[!] Error en la cadena de producción: {e}")


if __name__ == "__main__":
    nombre_archivo = "Reporte_GraphUG.md"
    if os.path.exists(nombre_archivo):
        ejecutar_pipeline(nombre_archivo)
    else:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")