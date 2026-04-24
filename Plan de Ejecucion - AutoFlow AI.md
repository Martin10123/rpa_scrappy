# Plan de Ejecucion - AutoFlow AI

### Proyecto universitario (version completa, no MVP)

---

## 1. Objetivo general

Desarrollar una plataforma funcional de automatizacion end-to-end basada en lenguaje natural que:

* Interprete instrucciones del usuario.
* Ejecute flujos de RPA sobre web.
* Procese y analice datos.
* Genere reportes Excel y visualizaciones.
* Entregue resultados en interfaz web y por correo.
* Mantenga historial reutilizable de ejecuciones.

---

## 2. Alcance del proyecto (version final)

### Incluido

* Frontend con input en lenguaje natural, panel de progreso y visualizacion de resultados.
* Backend API con ejecucion en background (asincrona simple).
* Parser IA (Claude API) para convertir instrucciones en JSON de pasos.
* Motor orquestador de pasos con control de estados y errores.
* Modulo RPA con Playwright.
* Modulo de procesamiento con Pandas + BeautifulSoup.
* Modulo de reportes Excel con OpenPyXL.
* Modulo de graficos con Matplotlib.
* Historial de flujos y resultados (BD).
* Notificaciones por correo con archivos adjuntos.
* Logs, manejo de errores y reintentos basicos.

### Fuera de alcance

* Multi-tenant empresarial.
* Escalado distribuido real.
* Marketplace o monetizacion.

---

## 3. Arquitectura objetivo (SIMPLIFICADA)

* Frontend: React + Vite
* Backend API: FastAPI
* Ejecucion de tareas: asyncio / BackgroundTasks
* Base de datos: PostgreSQL (SQLite en local)
* IA parser: Claude API (Anthropic)
* Automatizacion web: Playwright (Python)
* Datos: Pandas + BeautifulSoup4
* Reportes: OpenPyXL
* Graficos: Matplotlib
* Email: SMTP (smtplib)

---

## 4. Plan por fases (checklist)

## Fase 0 - Preparacion y gestion (Semana 1)

* [ ] Definir equipo y roles.
* [ ] Definir metodologia de trabajo.
* [ ] Crear repositorio y estrategia de ramas.
* [ ] Configurar entorno local.
* [ ] Definir convenciones de codigo.
* [ ] Definir Definition of Done.

**Entregable:**

* Repo base operativo.

---

## Fase 1 - Base tecnica del sistema (Semanas 2 y 3)

* [ ] Crear backend FastAPI modular.
* [ ] Endpoint POST /run
* [ ] Endpoint GET /status/{job_id}
* [ ] Implementar ejecucion en background (asyncio)
* [ ] Crear frontend base.
* [ ] Conectar frontend con backend.
* [ ] Definir modelos de datos.
* [ ] Configurar base de datos.

**Entregable:**

* Flujo: crear job → ejecutar → consultar estado.

---

## Fase 2 - Parser IA (Semanas 4 y 5)

* [ ] Cliente Claude API.
* [ ] Prompt robusto.
* [ ] Definir JSON de pasos.
* [ ] Validacion con Pydantic.
* [ ] Manejo de ambiguedades.
* [ ] Pruebas en español e ingles.

**Entregable:**

* Texto → JSON validado.

---

## Fase 3 - RPA + Extraccion (Semanas 6 y 7)

* [ ] Acciones: open_web, click, fill, wait, screenshot.
* [ ] Scraping de datos.
* [ ] Selectores + fallback.
* [ ] Reintentos y timeouts.
* [ ] Manejo de errores DOM.
* [ ] Pruebas controladas.

**Entregable:**

* Extraccion estable.

---

## Fase 4 - Datos y reportes (Semanas 8 y 9)

* [ ] Limpieza con Pandas.
* [ ] Calculos basicos.
* [ ] Excel con OpenPyXL.
* [ ] Graficos con Matplotlib.
* [ ] Guardar outputs.
* [ ] Exponer descargas.

**Entregable:**

* Datos + Excel + graficos.

---

## Fase 5 - Orquestador y progreso (Semanas 10 y 11)

* [ ] Estados: pending / running / success / error.
* [ ] Logs por paso.
* [ ] Guardar progreso en BD.
* [ ] Endpoint de polling.
* [ ] (Opcional) SSE.
* [ ] UI con progreso.
* [ ] Cancelacion basica.

**Entregable:**

* Ejecucion completa con feedback.

---

## Fase 6 - Historial y cierre (Semana 12)

* [ ] Persistir historial.
* [ ] Vista de historial.
* [ ] Re-ejecucion.
* [ ] Envio por correo.
* [ ] Resumen automatico.
* [ ] Seguridad basica.

**Entregable:**

* Sistema completo funcional.

---

## Fase 7 - QA y presentacion (Semanas 13 y 14)

* [ ] Pruebas por modulo.
* [ ] Pruebas end-to-end.
* [ ] Pruebas de carga basica.
* [ ] Correccion de bugs.
* [ ] Documentacion.
* [ ] Demo final.

**Entregable:**

* Version estable + demo.

---

## 5. Checklist de calidad

* [ ] Validacion en APIs.
* [ ] Logs completos.
* [ ] Errores claros.
* [ ] No secrets hardcodeados.
* [ ] Variables documentadas.
* [ ] Tests basicos.
* [ ] README actualizado.

---

## 6. Riesgos y mitigacion

* DOM cambia → selectores robustos.
* Bloqueos web → usar sitios controlados.
* Falla IA → retry + fallback.
* Tareas largas → asyncio + timeouts.
* Datos inconsistentes → validacion central.
* Retrasos → entregas semanales.

---

## 7. Definition of Done

* [ ] Flujo completo funcional.
* [ ] Excel + grafico generados.
* [ ] Progreso visible en frontend.
* [ ] Historial disponible.
* [ ] Manejo de errores correcto.
* [ ] Demo en vivo funcional.
* [ ] Documentacion entregada.

---

## 8. Rutina semanal

* [ ] Planificacion semanal.
* [ ] Seguimiento intermedio.
* [ ] Demo interna.
* [ ] Actualizacion de riesgos.
* [ ] Cierre semanal.

---

## 9. Evidencias

* [ ] Video demo.
* [ ] Capturas.
* [ ] JSON generado.
* [ ] Excel y grafico.
* [ ] Historial en BD.
* [ ] Metricas.
