# Diagnóstico y Refactorización

## 1. Contexto
* **Equipo:** [Escribe aquí tu nombre/equipo]
* **Repositorio:** [Pega aquí el enlace a tu GitHub]
* **Funcionalidad:** Procesamiento de Ventas (EcoVida POS).
* **Requisitos:** Registrar ventas, calcular descuentos según afiliación y actualizar inventario.

## 2. Arquitectura real
* **Componentes:** Controladores (main.py), Modelos (models.py) y Servicios (services.py).
* **Flujo:** El cliente web envía la orden; FastAPI valida con Pydantic; el servicio procesa la lógica de negocio y almacena la venta en memoria.

## 3. Hallazgos
**ID:** H-01 | **Tipo:** defecto
* **Ubicación:** services.py, EcoVidaService, procesar_venta
* **Evidencia:** `"fechaHora": "2026-10-19 18:26:00"`
* **Observación:** La fecha de la transacción está estática en el código. Todas las ventas quedan registradas en el mismo instante.
* **Criterio:** Defecto funcional que arruina el historial.
* **Impacto y riesgo:** Alto (3).
* **Acción propuesta:** Inyectar fecha dinámica del sistema.
* **Verificación:** Procesar ventas y revisar endpoints.
* **Estado:** seleccionado.

**ID:** H-02 | **Tipo:** deuda técnica
* **Ubicación:** services.py, EcoVidaService, registrar_cliente
* **Evidencia:** `if not cliente_data.cedula.isdigit():`
* **Observación:** Validación manual que repite lo que ya hace Pydantic en models.py.
* **Criterio:** Viola el principio DRY y la separación de responsabilidades.
* **Impacto y riesgo:** Medio (2).
* **Acción propuesta:** Eliminar validaciones manuales.
* **Verificación:** Enviar peticiones incorrectas y confirmar rechazo automático.
* **Estado:** pendiente.

**ID:** H-03 | **Tipo:** riesgo arquitectónico
* **Ubicación:** services.py, EcoVidaService, __init__
* **Evidencia:** `self.clientes = [...]`
* **Observación:** La capa de servicio almacena los datos, actuando como base de datos.
* **Criterio:** Viola Inversión de Dependencias (SOLID).
* **Impacto y riesgo:** Alto (3). Impide escalar el sistema.
* **Acción propuesta:** Extraer persistencia a un repositorio.
* **Verificación:** Ejecutar pruebas de los endpoints.
* **Estado:** pendiente.

## 4. Priorización
Se prioriza el hallazgo **H-01**.
* **Impacto:** 3 (Corrompe el historial y la facturación).
* **Riesgo:** 1 (Cambio seguro, no rompe otras clases).
* **Esfuerzo:** 1 (Baja complejidad técnica).

## 5. Intervención
* **Cambio elegido:** Generación dinámica del timestamp en la venta.
* **Archivos afectados:** services.py
* **Diseño antes:** String "2026-10-19 18:26:00".
* **Diseño después:** Uso de `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.

## 6. Verificación
Se realizaron ventas de prueba. Se validó en la ruta GET `/ventas` que cada registro posee su propia estampa de tiempo actual, conservando el cálculo de totales original.

## 7. Cierre
* **Lecciones:** Es vital eliminar datos de prueba quemados antes de integrar código.
* **Deuda pendiente:** Extraer la base de datos a un repositorio aparte.
* **Respuesta pregunta de cierre:** La práctica de revisiones de código (Code Review) o pruebas unitarias automatizadas habría detectado este problema antes del paso a producción.

## 8. Git
* **Commit Diagnóstico:** [Pegar hash tras el Paso 3]
* **Commit Refactorización:** [Pegar hash tras el Paso 5]
* **Commit Verificación:** [Pegar hash tras el Paso 5]
