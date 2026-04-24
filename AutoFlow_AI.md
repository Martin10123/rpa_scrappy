# AutoFlow AI
### Automatización inteligente de procesos mediante lenguaje natural

> **"El usuario describe lo que necesita. AutoFlow AI lo ejecuta."**

---

## ¿Qué es AutoFlow AI?

AutoFlow AI es una plataforma que permite automatizar procesos completos a partir de una instrucción escrita en lenguaje natural. Sin código. Sin configuración. Sin herramientas separadas.

El usuario escribe lo que necesita, y el sistema interpreta, planifica y ejecuta automáticamente: navega webs, extrae datos, genera reportes en Excel, crea gráficos, envía correos y muestra los resultados — todo en un solo lugar.

---

## El Problema

Automatizar un proceso hoy requiere combinar múltiples herramientas y perfiles técnicos especializados:

- Herramientas distintas para RPA, datos, reportes y visualización
- Alta dependencia de desarrolladores para cualquier cambio
- Procesos manuales repetitivos que consumen horas de trabajo semanales
- Costos elevados de implementación y mantenimiento
- Integración frágil entre herramientas que se rompe constantemente

**AutoFlow AI elimina todas esas barreras con una sola instrucción de texto.**

---

## Funcionalidades

### 🌐 1. Automatización Web (RPA) con IA

El sistema opera un navegador real de forma autónoma, sin intervención humana:

- Navegación autónoma a cualquier URL indicada por el usuario
- Extracción inteligente de tablas, listas, precios, textos e imágenes de páginas web
- Llenado automático de formularios con datos suministrados por el usuario
- Descarga automática de archivos desde portales web
- Manejo de páginas dinámicas con JavaScript (SPAs, React, Angular)
- Captura de pantalla de páginas completas o secciones específicas
- Detección y manejo automático de popups, cookies y banners de consentimiento
- Reintentos automáticos ante fallos de carga o elementos no disponibles

---

### 📊 2. Procesamiento y Análisis de Datos

Una vez recopilados los datos, el sistema los procesa y analiza de forma automática:

- Limpieza automática: eliminación de duplicados, corrección de formatos y normalización
- Cálculos estadísticos: promedio, suma, mínimo, máximo, mediana y percentiles
- Filtrado y segmentación de datos por cualquier criterio en lenguaje natural
- Cruce y combinación de datos provenientes de múltiples fuentes
- Detección de valores atípicos y anomalías
- Transformaciones: conversión de monedas, unidades, fechas y formatos de texto
- Agrupaciones y tablas dinámicas generadas automáticamente

---

### 📁 3. Generación de Reportes en Excel

AutoFlow AI genera archivos Excel profesionales y listos para entregar:

- Archivos `.xlsx` con datos estructurados y formateados automáticamente
- Estilos aplicados: colores, fuentes, bordes y ancho de columnas
- Múltiples hojas temáticas dentro del mismo archivo
- Fórmulas Excel nativas insertadas (SUMA, PROMEDIO, BUSCARV, etc.)
- Tablas dinámicas y gráficos incrustados directamente en el Excel
- Encabezados congelados para mejor navegación
- Descarga inmediata del archivo desde el navegador

---

### 📈 4. Visualización de Datos

Generación automática de gráficos de alta calidad sin configuración manual:

- Gráficos de barras, líneas, torta, dispersión, histogramas y mapas de calor
- Selección automática del tipo de gráfico más adecuado según los datos
- Personalización de colores, etiquetas, títulos y leyendas
- Gráficos interactivos visualizables directamente en el navegador
- Exportación como imagen (`.png`, `.svg`) o incrustados en el Excel
- Comparativas visuales entre múltiples conjuntos de datos

---

### ⚡ 5. Ejecución en Tiempo Real con Feedback Visual

El usuario ve exactamente qué está haciendo el sistema en cada momento:

- Panel de progreso con cada paso del flujo visible en tiempo real
- Indicador de estado por paso: pendiente → en ejecución → completado → error
- Log de actividad en vivo con las acciones ejecutadas
- Tiempo de ejecución estimado y tiempo transcurrido por paso
- Notificación instantánea al finalizar o ante cualquier error
- Posibilidad de pausar o cancelar un flujo en ejecución

---

### 🧠 6. Parser de Instrucciones con IA (Claude API)

El corazón de la plataforma: entender lenguaje humano y convertirlo en acciones ejecutables:

- Interpretación de instrucciones en español e inglés
- Descomposición automática de instrucciones complejas en pasos ordenados
- Validación del plan antes de ejecutarlo, con confirmación del usuario
- Manejo de ambigüedades: el sistema pregunta si algo no está claro
- Generación automática de selectores CSS para scraping adaptativo a cualquier web
- Adaptación del flujo si un paso falla, buscando alternativas antes de reportar error

---

### 🕓 7. Historial y Reutilización de Flujos

AutoFlow AI recuerda lo que el usuario ha ejecutado anteriormente:

- Registro histórico de todos los flujos con fecha, instrucción y resultado
- Re-ejecución de flujos anteriores con un solo clic
- Edición de instrucciones pasadas para ajustar parámetros sin reescribir
- Exportación del historial en CSV o PDF

---

### 📧 8. Notificaciones y Entrega de Resultados

Los resultados se entregan donde el usuario los necesita:

- Envío automático por correo electrónico del reporte Excel y gráficos generados
- Descarga directa desde el navegador de todos los archivos producidos
- Vista previa del Excel y de los gráficos embebida en la interfaz, sin descarga
- Resumen textual generado por IA: *"Se encontraron 47 productos. El precio promedio es $32.500."*

---

## Casos de Uso

| Industria | Instrucción de ejemplo | Output generado |
|-----------|------------------------|-----------------|
| Retail | "Extrae todos los productos de esta tienda con sus precios y genera un Excel con gráfico comparativo" | Excel + gráfico de precios |
| Recursos Humanos | "Descarga los reportes de asistencia del mes y calcula el ausentismo por área" | Análisis + reporte |
| Finanzas | "Descarga las tasas de cambio de hoy, conviértelas a COP y guárdalas en Excel" | Archivo `.xlsx` actualizado |
| Investigación | "Extrae todos los artículos publicados en 2024 con títulos, autores y fechas" | Base de datos estructurada |
| Logística | "Llena el formulario de seguimiento con estos 20 números de guía y exporta los estados" | Reporte de estados |

---

## Flujo de Demostración

**Instrucción:** *"Ve a esta página, extrae los productos con sus precios, guárdalo en Excel, calcula el precio promedio y genera un gráfico de barras."*

| Paso | Acción | Resultado |
|------|--------|-----------|
| 1️⃣ | Claude API interpreta la instrucción | Plan de ejecución en JSON |
| 2️⃣ | Playwright abre la URL indicada | Navegador activo |
| 3️⃣ | Se extraen nombres y precios | Datos estructurados |
| 4️⃣ | Se genera el archivo `.xlsx` | Reporte profesional listo |
| 5️⃣ | Pandas calcula el precio promedio | Métrica incluida en reporte |
| 6️⃣ | Matplotlib genera el gráfico de barras | Imagen embebida en resultado |
| 7️⃣ | El usuario descarga Excel y ve el gráfico | Resultado entregado |

---

## Stack Tecnológico

| Capa | Tecnología | Rol |
|------|------------|-----|
| IA / Parser | Claude API (Anthropic) | Interpreta lenguaje natural y genera flujos |
| RPA | Playwright (Python) | Automatización de navegador web |
| Datos | Pandas + BeautifulSoup4 | Procesamiento y análisis de datos |
| Reportes | OpenPyXL | Generación de archivos Excel profesionales |
| Gráficos | Matplotlib | Visualizaciones de alta calidad |
| Backend | FastAPI + Celery + Redis | API REST + ejecución asíncrona |
| Frontend | React + Vite | Interfaz con feedback en tiempo real |
| Notificaciones | SMTP (smtplib) | Envío de resultados por correo |
| Base de datos | PostgreSQL / SQLite | Historial de flujos y resultados |

---

## Innovación y Diferenciadores

- **Interfaz 100% en lenguaje natural** — no se requiere conocimiento técnico de ningún tipo
- **Integración real** de RPA + datos + reportes + visualización en un solo flujo
- **Retroalimentación en tiempo real** — el usuario ve cada acción mientras ocurre
- **Scraping adaptativo** — la IA genera los selectores automáticamente para cualquier web
- **Arquitectura modular** — cada tipo de acción es un módulo independiente y extensible
- **Gestión inteligente de errores** — si un paso falla, el sistema busca alternativas antes de detenerse
- **Historial reutilizable** — los flujos exitosos quedan guardados y se pueden volver a ejecutar
- **Entrega multicanal** — pantalla, descarga directa y correo electrónico

---

> *AutoFlow AI: de la instrucción al resultado, sin código, sin configuración, en segundos.*
