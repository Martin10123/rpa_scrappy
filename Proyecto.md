# AutoFlow AI
### Automatización End-to-End con Lenguaje Natural + RPA

---

## Descripción General

**AutoFlow AI** es una plataforma que permite automatizar procesos completos a partir de instrucciones en lenguaje natural.

El usuario describe lo que necesita hacer. El sistema interpreta la instrucción, la traduce a un flujo de acciones y lo ejecuta automáticamente — sin que el usuario escriba una sola línea de código.

Un flujo puede incluir:

- Interacción con páginas web (RPA con Playwright)
- Extracción y procesamiento de datos
- Generación de archivos Excel
- Visualización de resultados (gráficos)

---

## Problema

Automatizar un proceso hoy requiere múltiples herramientas separadas: una para RPA, otra para procesar datos, otra para generar reportes. Esto implica:

- Alta complejidad técnica
- Dependencia de perfiles especializados
- Procesos manuales y repetitivos
- Baja eficiencia operativa

No existe una solución unificada, accesible y de bajo costo que permita a usuarios no técnicos automatizar flujos completos.

---

## Solución

AutoFlow AI unifica todo en una sola plataforma que:

1. Recibe una instrucción en lenguaje natural
2. La interpreta y la convierte en pasos ejecutables
3. Ejecuta cada paso automáticamente (web, datos, archivos, gráficos)
4. Entrega un resultado tangible al usuario

---

## Caso de uso principal (demo)

**Instrucción del usuario:**
> "Ve a esta página, extrae los productos con sus precios, guárdalo en Excel, calcula el precio promedio y genera un gráfico de barras."

**Lo que ejecuta el sistema:**

| Paso | Acción | Herramienta |
|------|--------|-------------|
| 1 | Abrir navegador y navegar a la URL | Playwright |
| 2 | Extraer nombres y precios de productos | Playwright + BeautifulSoup |
| 3 | Guardar datos estructurados en Excel | OpenPyXL / Pandas |
| 4 | Calcular precio promedio | Pandas |
| 5 | Generar gráfico de barras | Matplotlib |
| 6 | Mostrar resultados al usuario | Respuesta de API / frontend |

**Output:**
- Archivo `.xlsx` descargable
- Gráfico de precios (imagen embebida o descargable)
- Resultado del cálculo (precio promedio)

---

## Arquitectura del sistema

```
[Usuario]
    |
    | instrucción en texto
    v
[Frontend] ──────────────────── React / HTML + CSS + JS
    |
    | POST /run (JSON con instrucción)
    v
[Backend API] ────────────────── FastAPI (Python)
    |
    |── [Parser de instrucción] ── Claude API (claude-haiku-3 o similar)
    |         |
    |         | JSON con pasos a ejecutar
    |         v
    |── [Orquestador de flujo] ── Lógica en Python
    |         |
    |         |── [Módulo RPA]       ── Playwright
    |         |── [Módulo de datos]  ── Pandas + BeautifulSoup
    |         |── [Módulo Excel]     ── OpenPyXL
    |         |── [Módulo de gráficos] ── Matplotlib
    |
    | resultado (archivos + datos)
    v
[Frontend] ── muestra resultado al usuario
```

---

## Stack Tecnológico

### Backend
- **Python 3.11+**
- **FastAPI** — API REST principal
- **Uvicorn** — servidor ASGI

### RPA
- **Playwright (Python)** — automatización de navegador

### Procesamiento de datos
- **Pandas** — manipulación de datos tabulares
- **BeautifulSoup4** — parsing de HTML extraído

### Generación de archivos
- **OpenPyXL** — escritura de archivos Excel (.xlsx)

### Visualización
- **Matplotlib** — generación de gráficos como imágenes

### Inteligencia artificial
- **Anthropic API (Claude)** — parsing de instrucciones en lenguaje natural → JSON de acciones
  - Modelo sugerido: `claude-haiku-3` o equivalente, optimizado para parsing rápido y económico

### Frontend
- **React + Vite** *(preferido)* o HTML + CSS + JS puro
- Comunicación con backend vía `fetch` / Axios

### Otros
- **python-dotenv** — manejo de variables de entorno (API keys)
- **JSON** — estructura interna de flujos

---

## Estructura del proyecto

```
autoflow-ai/
├── backend/
│   ├── main.py                  # Entry point FastAPI
│   ├── router.py                # Rutas API
│   ├── parser/
│   │   └── instruction_parser.py  # Llama a Claude API y devuelve JSON de pasos
│   ├── orchestrator/
│   │   └── flow_runner.py       # Ejecuta los pasos en orden
│   ├── modules/
│   │   ├── rpa.py               # Playwright: abrir web, extraer datos
│   │   ├── data_processing.py   # Pandas: limpiar y calcular
│   │   ├── excel_writer.py      # OpenPyXL: generar .xlsx
│   │   └── chart_generator.py   # Matplotlib: generar gráfico
│   ├── outputs/                 # Archivos generados (Excel, imágenes)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── InputBox.jsx     # Caja de texto para instrucción
│   │   │   ├── StepList.jsx     # Muestra pasos detectados
│   │   │   └── ResultPanel.jsx  # Muestra Excel + gráfico
│   │   └── api.js               # Llamadas al backend
│   └── package.json
└── README.md
```

---

## Formato de comunicación interna (JSON de flujo)

El parser convierte la instrucción del usuario en este formato:

```json
{
  "steps": [
    {
      "id": 1,
      "action": "open_web",
      "params": { "url": "https://ejemplo.com/productos" }
    },
    {
      "id": 2,
      "action": "scrape_data",
      "params": { "selector": ".producto", "fields": ["nombre", "precio"] }
    },
    {
      "id": 3,
      "action": "save_excel",
      "params": { "filename": "productos.xlsx" }
    },
    {
      "id": 4,
      "action": "calculate",
      "params": { "operation": "average", "field": "precio" }
    },
    {
      "id": 5,
      "action": "generate_chart",
      "params": { "type": "bar", "x": "nombre", "y": "precio" }
    }
  ]
}
```

---

## MVP — Alcance de entrega

### Incluye:
- [ ] Input de texto en el frontend
- [ ] Llamada a Claude API para parsear la instrucción
- [ ] Ejecución de Playwright en una web controlada (por ejemplo, una página de productos estática)
- [ ] Extracción de datos (nombre + precio)
- [ ] Guardado en Excel (.xlsx)
- [ ] Cálculo de precio promedio
- [ ] Generación de gráfico de barras
- [ ] Visualización del resultado en el frontend (descarga de Excel e imagen del gráfico)

### No incluye (fuera de alcance):
- Automatización de webs arbitrarias (solo la web de demo)
- Autenticación de usuarios
- Guardado persistente de flujos
- IA generativa de flujos complejos
- Marketplace

---

## Plan de desarrollo sugerido

| Semana | Objetivo |
|--------|----------|
| 1 | Configuración del proyecto. Backend con FastAPI en ejecución. El endpoint `/run` recibe texto y retorna JSON fijo. |
| 2 | Integración con Claude API. El parser convierte una instrucción real en JSON de pasos. |
| 3 | Implementación de módulos: RPA (Playwright) y extracción de datos (BeautifulSoup). |
| 4 | Implementación de módulos: Excel (OpenPyXL) y gráficos (Matplotlib). |
| 5 | Orquestador: ejecuta los pasos en orden a partir del JSON. |
| 6 | Frontend básico: input, visualización de pasos y resultado. |
| 7 | Integración completa y pruebas del flujo end-to-end. |
| 8 | Pulido final, demo preparada y documentación. |

---

## API — Endpoint principal

```
POST /run
Content-Type: application/json

{
  "instruction": "Extrae los productos de https://demo.com, guárdalos en Excel y genera un gráfico de precios"
}
```

**Response:**
```json
{
  "steps_executed": ["open_web", "scrape_data", "save_excel", "calculate", "generate_chart"],
  "results": {
    "average_price": 45200,
    "excel_url": "/outputs/productos.xlsx",
    "chart_url": "/outputs/grafico_precios.png"
  },
  "status": "success"
}
```

---

## Variables de entorno (.env)

```env
ANTHROPIC_API_KEY=sk-...
DEMO_WEB_URL=https://url-de-la-web-de-prueba.com
OUTPUT_DIR=./outputs
```

---

## Innovación

- **Interfaz en lenguaje natural** como único punto de entrada
- **Integración real** de RPA + datos + archivos + visualización en un solo flujo
- **Eliminación de barreras técnicas** para usuarios no programadores
- **Arquitectura modular** que permite escalar fácilmente con nuevos tipos de acciones

---

## Pitch

> AutoFlow AI permite automatizar procesos completos a partir de una instrucción en lenguaje natural. El usuario describe lo que necesita y el sistema ejecuta automáticamente la navegación web, la extracción de datos, la generación de Excel y la visualización de resultados, sin código, sin configuración y en segundos.

---
