# Diagnóstico y Refactorización

## 1. Contexto
* **Equipo:** Juan Herrera
* **Repositorio:** [(https://github.com/Juan001-H/Eco-Vida-Softare-Proyecto)]
* **Funcionalidad:** Procesamiento de Ventas y Gestión de Clientes (EcoVida POS).
* **Requisitos:** Registrar ventas, calcular descuentos según afiliación y actualizar inventario.

## 2. Arquitectura real
* **Componentes:** Controladores (main.py), Modelos (models.py) y Servicios (services.py).
* **Flujo:** El cliente web envía la orden; FastAPI valida con Pydantic; el servicio procesa la lógica de negocio y almacena en memoria.

## 3. Hallazgos
**ID:** H-01 | **Tipo:** defecto
* **Ubicación:** services.py, EcoVidaService, procesar_venta
* **Evidencia:** `"fechaHora": "2026-10-19 18:26:00"`
* **Observación:** La fecha de la transacción está estática en el código. Todas las ventas quedan registradas en el mismo instante.
* **Criterio:** Defecto funcional que arruina el historial.
* **Impacto y riesgo:** Alto (3).
* **Acción propuesta:** Inyectar fecha dinámica del sistema.
* **Verificación:** Procesar ventas y revisar endpoints.
* **Estado:** implementado y verificado.

**ID:** H-02 | **Tipo:** deuda técnica
* **Ubicación:** services.py, EcoVidaService, registrar_cliente y actualizar_cliente
* **Evidencia:** `if not cliente_data.cedula.isdigit():`
* **Observación:** Validación manual que repite lo que ya hace Pydantic en models.py.
* **Criterio:** Viola el principio DRY y la separación de responsabilidades.
* **Impacto y riesgo:** Medio (2).
* **Acción propuesta:** Eliminar validaciones manuales.
* **Verificación:** Enviar peticiones incorrectas y confirmar rechazo automático.
* **Estado:** implementado y verificado.

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
Se priorizan los hallazgos **H-01 y H-02** para el alcance del taller.
* **Impacto:** 3 (Corrompe historial) y 2 (Violación DRY).
* **Riesgo:** 1 (Cambios seguros).
* **Esfuerzo:** 1 (Baja complejidad técnica).

## 5. Intervención
* **Cambio elegido 1:** Generación dinámica del timestamp en la venta. Se usó `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.
* **Cambio elegido 2:** Eliminación de los `if` de validación regex/isdigit en los métodos de cliente del servicio.
* **Archivos afectados:** services.py

## 6. Verificación
Se realizaron pruebas sobre el endpoint GET `/ventas` confirmando estampas de tiempo correctas. Al crear clientes con datos inválidos, FastAPI arroja automáticamente el error HTTP 422 configurado en los esquemas, demostrando que la seguridad del sistema se mantiene tras limpiar el código redundante del servicio.

## 7. Cierre
* **Lecciones:** Es vital delegar responsabilidades al framework correcto y eliminar datos quemados.
* **Deuda pendiente:** Extraer la base de datos a un repositorio aparte.
* **Respuesta pregunta de cierre:** La práctica de revisiones de código (Code Review) y pruebas unitarias habría detectado estos problemas.

## 8. Git
* **Commit Diagnóstico:** b1c96ec
* **Commit Refactorización (Fecha):** 8c7
* **Commit Refactorización (Validaciones):** [Hash generado tras el paso 1]

## 9. Sustentación (Segunda Parte)
**1. ¿Cuál era el problema identificado y dónde estaba localizado?** 
El H-01 consistía en fechas estáticas ("quemadas") en el método `procesar_venta`. El H-02 trataba de validaciones de formato manuales (regex e isdigit) dentro de `registrar_cliente` y `actualizar_cliente` en el archivo `services.py` que repetían el trabajo de Pydantic.

**2. ¿Qué principio de diseño o atributo de calidad estaba comprometido?**
En H-01 se afectaba la mantenibilidad e integridad de los datos. En H-02 se violaba el principio DRY (Don't Repeat Yourself) y el Principio de Responsabilidad Única (SRP), mezclando lógica de negocio con validación de datos.

**3. ¿Qué modificación realizaron y cómo cambiaron las responsabilidades o dependencias?**
En H-01 se inyectó la librería `datetime`. En H-02 se borraron los condicionales manuales del servicio. Las responsabilidades quedaron claras: el modelo (`models.py`) valida los datos a través de Pydantic, y el servicio (`services.py`) procesa reglas de negocio confiando en que los datos ya están saneados.

**4. ¿Qué consecuencias tiene el cambio sobre la arquitectura de la aplicación?**
Mejora la cohesión de las capas. La capa de servicio quedó más limpia, desacoplada y enfocada exclusivamente en su responsabilidad central, facilitando pruebas y mantenimiento futuro.

**5. ¿Qué evidencias demuestran que la funcionalidad conserva su comportamiento?**
Al probar el sistema, las facturas se siguen generando pero ahora con la estampa de tiempo actual del sistema operativo. Al enviar clientes con datos inválidos, el sistema sigue rechazándolos y retorna un error HTTP automático, demostrando que las reglas del negocio siguen protegidas.
