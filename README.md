# .MD to .PDF Compiler: Automatización de Documentos Científicos con Pandoc y LuaLaTeX

Este proyecto es una herramienta de automatización (CI/CD para documentos) diseñada para convertir apuntes y reportes técnicos escritos en formato Markdown (ej. Obsidian) en documentos PDF de grado científico y archivos DOCX editables. 

Utiliza **Pandoc** y **LuaLaTeX** como motores principales, aplicando una plantilla tipográfica rigurosa (estilo artículo académico a una columna) y un script de post-procesamiento en Python que corrige automáticamente los desbordamientos clásicos de LaTeX en tablas y bloques de código.

## Características Principales

* **Generación Multiformato:** Compila simultáneamente un archivo `.tex` (código fuente), un `.pdf` (listo para imprenta) y un `.docx` (borrador editable).
* **Plantilla Científica:** Diseño a una sola columna, tipografía con serifa (Times), márgenes estrictos y jerarquía de títulos formal (I, A, 1).
* **Post-Procesamiento Automático:**
  * Intercepta y reescribe entornos `longtable` para que las tablas grandes se ajusten al ancho exacto de la página usando `adjustbox`.
  * Reduce dinámicamente el tamaño de fuente en bloques de código (`Shaded`, `verbatim`) para evitar el error *Overfull \hbox*.
* **Limpieza de Entorno:** Elimina automáticamente la "basura" de compilación de LaTeX (`.aux`, `.log`, `.out`, etc.) manteniendo el directorio de trabajo limpio.

## Requisitos del Sistema

Para que la cadena de producción funcione, el entorno (Windows/Linux) debe contar con las siguientes herramientas instaladas:

1. **Python 3.10+**
2. **Pandoc:** Motor universal de conversión de documentos.
3. **Distribución LaTeX (MiKTeX o TeX Live):** Necesario para el motor `lualatex`.
4. **Dependencia de Python:** Librería `pypandoc`.

**Instalación rápida en Windows (PowerShell):**
```powershell
winget install --id JohnMacFarlane.Pandoc
winget install --id MiKTeX.MiKTeX
pip install pypandoc
```
*(Nota: Configurar MiKTeX para instalar paquetes "On-the-fly" o "Sobre la marcha").*

## Estructura del Directorio

Tu espacio de trabajo debe contener al menos los siguientes archivos:

```text
📁 Proyecto/
├── 📄 MD_Tex_tD.py.py              # Script principal de la cadena de producción
├── 📄 plantilla_profesional.tex    # Plantilla de diseño LaTeX
└── 📄 Reporte_Proyecto.md          # Tu documento fuente escrito en Markdown
```

## Guía de Escritura en Markdown

Para que la automatización no requiera intervención manual, el archivo `.md` debe cumplir con las siguientes especificaciones:

### 1. Metadatos (YAML Frontmatter)
El archivo debe comenzar obligatoriamente con el siguiente bloque de metadatos, el cual alimenta la portada y los encabezados del PDF:

```yaml
---
title: " "
author: " "
degree: " "
course: " "
university: " "
date: " "
location: " "
email: " "
header-left: " "
---
```

### 2. Jerarquía de Títulos
Utilizar únicamente las marcas de Markdown para títulos. **No numerar los títulos manualmente**, la plantilla LaTeX lo hará automáticamente:
* `# Título Principal` -> **I. TÍTULO PRINCIPAL**
* `## Subtítulo` -> **A. Subtítulo**
* `### Apartado` -> **1) Apartado**

### 3. Fórmulas y Matemáticas
Usar la sintaxis estándar de LaTeX encerrada en signos de dólar `$$...$$` para bloques de ecuaciones, y `$ ... $` para matemáticas en línea. Al ser un formato de una columna, las matrices y ecuaciones largas (como entornos `cases`) encajarán perfectamente.

### 4. Tablas
Dibujar las tablas en Markdown estándar. El script de Python detectará la tabla y la inyectará en un entorno `table` ajustado al `\textwidth`. No intentes darles formato de ancho en el Markdown.

## Uso

Con un archivo `.md` cumpliendo las especificaciones anteriores:

1. Especificar el nombre del archivo Markdown en la variable `nombre_archivo` dentro de `MD_Tex_tD.py`.
2. Activar entorno virtual (si aplica).
3. Ejecutar el programa:

```bash
python MD_Tex_tD.py
```

El script imprimirá el progreso fase por fase y, al finalizar, tendrá archivos `.pdf`, `.docx` y `.tex` generados en el mismo directorio.
