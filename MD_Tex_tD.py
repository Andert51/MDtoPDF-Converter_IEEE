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
        '-V', 'lang=es-ES'
    ]

    try:
        print(f"[*] Iniciando producción de documentos para: {input_md}")

        # FASE 1: Generación de DOCX para edición rápida
        pypandoc.convert_file(input_md, 'docx', outputfile=output_docx)

        # FASE 2: Traducción a LaTeX
        pypandoc.convert_file(input_md, 'latex', outputfile=output_tex, extra_args=args_pdf)

        # FASE 3: Post-Procesamiento (Garantía de legibilidad)
        with open(output_tex, 'r', encoding='utf-8') as f:
            tex_data = f.read()

        # Forzar ajuste de tablas al ancho de página
        tex_data = tex_data.replace(r'\begin{longtable}[]',
                                    r'\begin{table}[htbp]\centering\begin{adjustbox}{max width=\textwidth}\begin{tabular}')
        tex_data = tex_data.replace(r'\begin{longtable}',
                                    r'\begin{table}[htbp]\centering\begin{adjustbox}{max width=\textwidth}\begin{tabular}')
        tex_data = tex_data.replace(r'\end{longtable}', r'\end{tabular}\end{adjustbox}\end{table}')

        for cmd in [r'\endhead', r'\endfirsthead', r'\endfoot', r'\endlastfoot']:
            tex_data = tex_data.replace(cmd, '')

        # Optimizar tamaño de fuentes en bloques técnicos
        tex_data = tex_data.replace(r'\begin{Shaded}', r'\begin{Shaded}\small')
        tex_data = tex_data.replace(r'\begin{verbatim}', r'\begin{verbatim}\small')

        with open(output_tex, 'w', encoding='utf-8') as f:
            f.write(tex_data)

        # FASE 4: Compilación PDF
        print(f"[*] Compilando PDF final con Lualatex...")
        subprocess.run(['lualatex', '--interaction=nonstopmode', output_tex],
                       capture_output=True, text=True, encoding='utf-8')

        # FASE 5: Limpieza selectiva
        for ext in ['.log', '.aux', '.out', '.fls', '.fdb_latexmk', '.synctex.gz']:
            if os.path.exists(f"{base}{ext}"): os.remove(f"{base}{ext}")

        print(f"\nPROCESO COMPLETADO: {output_pdf} y {output_docx} creados exitosamente...")

    except Exception as e:
        print(f"\n[!] Error en la cadena de producción: {e}")


if __name__ == "__main__":
    nombre_archivo = "Reporte_GraphUG.md"
    if os.path.exists(nombre_archivo):
        ejecutar_pipeline(nombre_archivo)