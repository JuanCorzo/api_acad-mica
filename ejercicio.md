# Retos para estudiantes: ampliar la API Académica

Estos retos parten de la API de cursos existente. El objetivo es completar su CRUD y aplicar la misma arquitectura a un nuevo recurso: estudiantes.

Resuelve los retos en orden. Aquí encontrarás el comportamiento esperado y pistas para avanzar; la implementación queda a tu cargo. Consulta el [README](README.md) para iniciar el proyecto y la [guía del proyecto](docs.md) para repasar su funcionamiento.

## Preparación

1. Activa el entorno virtual e inicia la API desde la carpeta que contiene `main.py`:

   ```bash
   python -m uvicorn main:app --reload
   ```

2. Abre http://127.0.0.1:8000/docs.
3. Comprueba que puedes crear y consultar cursos.
4. Crea registros de práctica y anota sus IDs. Los IDs de los ejemplos son ilustrativos: usa los que devuelva tu API.

En cada reto, conserva la separación de responsabilidades: **router → servicio → base de datos**, con esquemas para validar entradas y definir salidas. Agrega comentarios que expliquen las decisiones relevantes.

## Reto 1. Eliminar un curso con DELETE

### Objetivo

Permitir que un cliente elimine un curso mediante su identificador y manejar correctamente los IDs inexistentes.

### Contrato del endpoint

| Elemento | Requisito |
| --- | --- |
| Método y ruta | `DELETE /courses/{course_id}` |
| Parámetro | `course_id` debe ser un entero. |
| Cuerpo de entrada | No se requiere. |
| Curso existente | Eliminar el registro y responder con `200 OK`. |
| Curso inexistente | Responder con `404` y `{"detail": "Course not found"}`. |
| ID no entero | Responder con `422`. |

La respuesta de una eliminación correcta debe ser:

```json
{
  "message": "Course deleted"
}
```

Para este reto se utiliza `200` porque se devuelve un mensaje JSON. Una respuesta `204` no debe incluir cuerpo y no corresponde al contrato elegido.

### Archivos que debes trabajar

- `services/course_service.py`: crear la función `delete_course`.
- `routers/courses.py`: importar el servicio y declarar el endpoint.

### Pistas

1. Revisa cómo `get_course` busca un registro y maneja su ausencia.
2. Investiga cómo eliminar una entidad con `session.delete()`.
3. Recuerda confirmar la transacción para que el cambio persista.
4. Devuelve el mensaje de éxito únicamente después de confirmar la eliminación.

### Pruebas de aceptación

| Prueba | Resultado esperado |
| --- | --- |
| Crear un curso y eliminarlo por su ID | `200` y mensaje de confirmación. |
| Consultar el curso eliminado | `404`. |
| Listar cursos después de eliminar | El registro ya no aparece y los demás permanecen. |
| Eliminar nuevamente el mismo ID | `404`. |
| Enviar un ID como `abc` | `422`. |
| Reiniciar Uvicorn y consultar el curso eliminado | Continúa sin existir. |

**Para explicar:** ¿qué diferencia hay entre quitar un objeto de una lista en memoria y eliminar un registro de SQLite? ¿Por qué necesitas confirmar la transacción?

## Reto 2. Actualizar un curso con PUT

### Objetivo

Modificar los datos de un curso existente sin crear otro registro ni cambiar su identificador.

En este reto, la actualización es completa: el cliente debe enviar `name`, `credits` y `active`. La actualización parcial con `PATCH` queda fuera del alcance.

### Contrato del endpoint

| Elemento | Requisito |
| --- | --- |
| Método y ruta | `PUT /courses/{course_id}` |
| Parámetro | `course_id` debe ser un entero. |
| Esquema de entrada | Crear `CourseUpdate`. |
| `name` | Obligatorio, entre 3 y 80 caracteres. |
| `credits` | Obligatorio, entero entre 1 y 6. |
| `active` | Obligatorio, booleano, sin valor predeterminado. |
| Respuesta correcta | `200 OK` con el curso actualizado según `CourseResponse`. |
| Curso inexistente con cuerpo válido | `404` y `{"detail": "Course not found"}`. |
| Datos inválidos o campos obligatorios ausentes | `422`. |

Ejemplo de cuerpo para `PUT /courses/1`:

```json
{
  "name": "Programación II",
  "credits": 4,
  "active": false
}
```

Si el curso con ID `1` existe, la respuesta esperada es:

```json
{
  "id": 1,
  "name": "Programación II",
  "credits": 4,
  "active": false
}
```

### Archivos que debes trabajar

- `schemas/course.py`: definir `CourseUpdate` con sus validaciones.
- `services/course_service.py`: crear la función `update_course`.
- `routers/courses.py`: declarar el endpoint y su modelo de respuesta.

### Pistas

1. Busca el curso por su clave primaria antes de modificarlo.
2. Trabaja sobre el objeto existente; construir uno nuevo podría producir una inserción.
3. Asigna los datos validados, confirma los cambios y recarga el registro.
4. No aceptes un nuevo ID como parte de los campos actualizables.
5. Un valor `false` también es un dato que debes guardar; no lo descartes por ser falso.

### Pruebas de aceptación

| Prueba | Resultado esperado |
| --- | --- |
| Actualizar un curso existente con datos válidos | `200` y los nuevos valores. |
| Consultar después el mismo ID | Los cambios aparecen y el ID se conserva. |
| Comparar la cantidad de cursos antes y después | No aumenta por la actualización. |
| Cambiar `active` de `true` a `false` | Se guarda `false`. |
| Usar un ID inexistente y un cuerpo válido | `404`. |
| Enviar créditos `0` o `7`, o nombre de 2 caracteres | `422`; el curso conserva sus valores anteriores. |
| Omitir `active` | `422`, porque en este reto es obligatorio. |
| Reiniciar y consultar | Los cambios permanecen. |

**Para explicar:** ¿por qué conviene separar `CourseCreate` de `CourseUpdate`? ¿Qué cambiaría si permitieras enviar solo uno de los campos?

Al completar los dos primeros retos tendrás el CRUD de cursos:

| Operación | Método y ruta |
| --- | --- |
| Crear | `POST /courses` |
| Leer | `GET /courses` y `GET /courses/{course_id}` |
| Actualizar | `PUT /courses/{course_id}` |
| Eliminar | `DELETE /courses/{course_id}` |

## Reto 3. Agregar el recurso Students

### Objetivo

Crear un recurso independiente llamado `Student`, reutilizando la organización del proyecto. Debes implementar creación y consulta de estudiantes, manteniendo el funcionamiento de los cursos.

Este reto no requiere relacionar estudiantes con cursos ni implementar matrículas, actualización o eliminación de estudiantes.

### Modelo y validaciones

| Campo | Requisito |
| --- | --- |
| `id` | Entero, clave primaria generada por la base de datos; no se solicita al crear. |
| `name` | Texto obligatorio, entre 3 y 80 caracteres. |
| `email` | Texto obligatorio no vacío. |
| `semester` | Entero obligatorio entre 1 y 10. |
| `active` | Booleano opcional en la creación; predeterminado `true`. |

Para el alcance básico, `email` se almacena como texto y se valida que no esté vacío. La validación de formato de correo y la unicidad quedan como ampliaciones opcionales; no se asumen implementadas.

### Archivos que debes crear

```text
models/student.py             # Modelo Student y tabla
schemas/student.py            # StudentCreate y StudentResponse
services/student_service.py   # Creación, listado y consulta por ID
routers/students.py            # Rutas con prefijo /students
```

También debes modificar `main.py` para importar y registrar el router de estudiantes. Usa la conexión y la dependencia de sesión existentes.

### Endpoints obligatorios

| Método y ruta | Resultado esperado |
| --- | --- |
| `POST /students` | `201` con el estudiante creado y su ID. |
| `GET /students` | `200` con una lista; `[]` si no hay estudiantes. |
| `GET /students/{student_id}` | `200` con el estudiante o `404` si no existe. |

Para un estudiante inexistente, devuelve:

```json
{
  "detail": "Student not found"
}
```

Los datos de entrada inválidos y los IDs no enteros deben producir `422`.

Ejemplo de cuerpo para `POST /students`:

```json
{
  "name": "Ana Pérez",
  "email": "ana@universidad.edu",
  "semester": 4
}
```

Respuesta ilustrativa:

```json
{
  "id": 1,
  "name": "Ana Pérez",
  "email": "ana@universidad.edu",
  "semester": 4,
  "active": true
}
```

### Pistas

1. Compara el propósito de `Course`, `CourseCreate` y `CourseResponse` antes de definir sus equivalentes.
2. Asegúrate de que el modelo `Student` se importe antes de ejecutar `create_db_and_tables()`; así su tabla queda registrada en los metadatos.
3. Recuerda que declarar un router no basta: debes incluirlo en la aplicación.
4. Usa `Student` en las consultas del nuevo servicio y revisa nombres, prefijos y mensajes al adaptar código.
5. La tabla nueva debe crearse en la misma base de datos sin borrar los cursos existentes.

### Pruebas de aceptación

| Prueba | Resultado esperado |
| --- | --- |
| Abrir Swagger | Aparecen las tres rutas de estudiantes y las rutas de cursos. |
| Crear un estudiante sin enviar `active` | `201`, ID generado y `active: true`. |
| Crear otro con `active: false` | Se conserva el valor `false`. |
| Listar y consultar por ID | Se recuperan los datos guardados. |
| Consultar un ID inexistente | `404` con el mensaje indicado. |
| Enviar semestre `0` u `11` | `422`. |
| Enviar nombre de 2 caracteres, email vacío u omitir email | `422`. |
| Reiniciar Uvicorn desde la misma carpeta | Los estudiantes siguen disponibles. |
| Consultar cursos después de agregar Students | Los cursos anteriores permanecen y sus endpoints funcionan. |

**Para explicar:** ¿qué partes reutilizaste y cuáles pertenecen exclusivamente a Students? ¿Por qué no necesitas crear otro motor de base de datos?

## Cómo documentar las pruebas y evidencias de ejecución

**Debes probar todos los endpoints, incluidos los que ya existían, y entregar un informe con sus resultados. Se aceptan capturas de pantalla de las ejecuciones como evidencia.** Puedes realizar las pruebas manualmente en Swagger, Postman o con `curl`; automatizarlas es opcional.

### 1. Prepara el informe

Puedes usar Markdown, Word o PDF. Incluye tu nombre, fecha, versión del proyecto que probaste, comando de inicio de Uvicorn, URL base y herramienta utilizada. Describe si la base de pruebas estaba vacía o tenía registros. Utiliza datos ficticios.

Organización sugerida para una entrega en Markdown:

```text
entrega-pruebas/
├── informe-pruebas.md
└── evidencias/
    ├── P01-crear-curso.png
    ├── P02-listar-cursos.png
    ├── P04-antes-update.png
    ├── P04-despues-update.png
    ├── P05-delete.png
    ├── P05-consulta-posterior.png
    └── P09-reinicio-uvicorn.png
```

Asigna un identificador a cada prueba y úsalo en los archivos de evidencia. Los nombres anteriores son ejemplos, no una lista completa de imágenes requeridas.

### 2. Registra todas las pruebas

Esta es la cobertura mínima del informe. Cada variante debe ejecutarse por separado, manteniendo válidos los demás datos. Por ejemplo, usa `P01a`, `P01b` y `P01c` para distinguir los casos de creación.

| Grupo | Endpoint o comprobación | Casos que debes documentar |
| --- | --- | --- |
| P01 | `POST /courses` | Datos válidos → `201`; omitir active → `true`; enviar active false → `false`; nombres de 3 y 80 caracteres y créditos 1 y 6 → aceptados; nombres de 2 y 81 caracteres, créditos 0 y 7, campos obligatorios ausentes → `422`. |
| P02 | `GET /courses` | Base de pruebas vacía → `200` y `[]`; varios cursos → lista con sus datos; incluir activos e inactivos. |
| P03 | `GET /courses/{course_id}` | ID existente → `200`; inexistente → `404`; ID `abc` → `422`. |
| P04 | `PUT /courses/{course_id}` | Datos válidos → `200`, mismo ID y misma cantidad de cursos; guardar active false; límites válidos e inválidos de nombre y créditos; omitir cada campo obligatorio → `422`; ID inexistente con cuerpo válido → `404`; ID `abc` → `422`. |
| P05 | `DELETE /courses/{course_id}` | Eliminar existente → `200` y mensaje; consultar después → `404`; lista sin el eliminado; otros cursos intactos; repetir DELETE o usar ID inexistente → `404`; ID `abc` → `422`. |
| P06 | `POST /students` | Datos válidos → `201`; active omitido → `true`; active false → `false`; nombres de 3 y 80 caracteres y semestres 1 y 10 → aceptados; nombres de 2 y 81 caracteres, semestres 0 y 11, email vacío y campos obligatorios ausentes → `422`. |
| P07 | `GET /students` | Base de pruebas vacía → `200` y `[]`; varios estudiantes → lista con sus datos, incluidos activos e inactivos. |
| P08 | `GET /students/{student_id}` | ID existente → `200`; inexistente → `404`; ID `abc` → `422`. |
| P09 | Persistencia e integración | Después de reiniciar: cursos y estudiantes creados permanecen, cambios de PUT permanecen y cursos eliminados siguen ausentes; las operaciones de cursos no modifican estudiantes ni viceversa. |

En POST y PUT prueba también tipos inválidos: `"abc"` en créditos o semestre y `"invalido"` en active deben producir `422`. Comprueba que una petición rechazada no cree registros ni cambie los datos existentes. Para Students no se exige validar el formato ni la unicidad del email en el alcance básico.

Registra una fila por ejecución:

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P01a | `POST /courses` | Nombre válido, créditos 3 | `201` e ID generado | Completar al ejecutar | Pendiente | Archivo o enlace |
| P01b | `POST /courses` | Créditos 0; resto válido | `422`, error en credits | Completar al ejecutar | Pendiente | Archivo o enlace |

Usa los estados **Pendiente**, **Aprobado** o **Fallido**. Un `422` esperado ante una entrada inválida es una prueba aprobada. Registra resultados reales, no supuestos.

### 3. Usa esta ficha para explicar cada ejecución

Puedes referenciar datos de la tabla para evitar repetirlos. Plantilla para un informe Markdown:

```markdown
### P01a — Crear un curso válido

- Fecha y hora: [momento de ejecución]
- Objetivo: comprobar la creación de un curso.
- Preparación: [estado inicial de la base de pruebas]
- Método y URL: POST http://127.0.0.1:8000/courses
- Datos enviados: [copiar el JSON exacto]
- Pasos: [acciones realizadas]
- Resultado esperado: HTTP 201, ID generado y datos enviados.
- Resultado obtenido: [código HTTP y cuerpo real de la respuesta]
- Comprobación posterior: [consulta realizada, si corresponde]
- Estado: [Pendiente / Aprobado / Fallido]
- Observaciones: [diferencias o correcciones]

![P01a: petición y respuesta de creación](evidencias/P01a-crear-curso.png)
```

La última línea inserta una imagen. La ruta debe coincidir con el archivo real y es relativa al informe. Entrega también la carpeta `evidencias`. En Word o PDF, inserta la captura junto a la explicación y coloca un pie con el identificador de la prueba.

### 4. Toma capturas que demuestren la ejecución

En Swagger:

1. Abre el endpoint y pulsa **Try it out**.
2. Introduce el ID o el cuerpo JSON del caso.
3. Pulsa **Execute**.
4. Captura la petición y la sección **Server response**, mostrando el estado HTTP y el cuerpo recibido.
5. Si no cabe todo, toma dos imágenes: una de la petición y otra de la respuesta, identificadas con el mismo caso.

La sección **Example Value** o las respuestas posibles de Swagger no demuestran una ejecución. Muestra la respuesta real obtenida después de pulsar **Execute**.

En Postman, captura el método, la URL, el cuerpo enviado cuando corresponda, el estado y la respuesta. En terminal, muestra el comando y su salida; `curl -i` permite incluir el estado HTTP. También se acepta la salida guardada como texto.

Las imágenes deben ser legibles y permitir relacionar los datos enviados con los recibidos. Una captura del código fuente o de Uvicorn encendido no demuestra por sí sola que un endpoint funcione.

### 5. Adjunta evidencias antes y después cuando corresponda

| Operación | Evidencias necesarias |
| --- | --- |
| Crear | POST con respuesta e ID generado; consulta posterior para comprobar el registro. |
| Consultar | GET con estado HTTP y objeto o lista recibida. |
| Actualizar | Datos anteriores, PUT y GET posterior con el mismo ID y los nuevos valores. |
| Eliminar | Registro existente, DELETE y GET posterior con `404`; lista sin ese ID. |
| Rechazar datos inválidos | Petición y `422`; consultas antes y después para comprobar que no se alteraron registros. |
| Probar persistencia | Consulta previa, terminal mostrando parada y nuevo inicio de Uvicorn, y consulta posterior de los mismos IDs. |

Usa la misma base de pruebas y el mismo directorio al reiniciar. Para comprobar listas vacías, utiliza una base de pruebas nueva; no borres datos que quieras conservar. Usa IDs reales devueltos por la API y verifica que los IDs elegidos como inexistentes no estén registrados.

Una captura puede respaldar varios casos si indicas expresamente cuáles y qué demuestra para cada uno.

### 6. Documenta los fallos y la repetición

Si una prueba falla, conserva la evidencia, explica la diferencia entre lo esperado y lo obtenido, corrige el problema y repite la prueba. Identifica los intentos, por ejemplo `P04-intento-1.png` y `P04-intento-2.png`.

Si automatizas, entrega el código de pruebas, el comando de ejecución y su salida, indicando qué casos cubre cada test. Antes de entregar, verifica que las imágenes se abran, que todas las variantes tengan resultado y que la evidencia corresponda a la versión final del proyecto.


## Entrega y criterios de revisión

Entrega el código de los tres retos y un informe de ejecución de todas las pruebas indicadas, incluidos los endpoints originales. Para cada caso y variante, registra la petición, el estado recibido, el resultado observado y su evidencia. Se aceptan capturas de pantalla acompañadas de su explicación.

La entrega debe incluir:

- Los endpoints solicitados, con los estados y respuestas definidos.
- Las validaciones y el manejo de recursos inexistentes.
- El informe con resultados de los ocho endpoints y evidencias vinculadas a cada caso.
- Las capturas o archivos de ejecución; si el informe es Markdown, incluye la carpeta de imágenes.
- Evidencia de que los cambios persisten después de reiniciar.
- La separación entre modelos, esquemas, servicios y routers.
- Las respuestas a las preguntas de explicación de cada reto.

Se revisará tanto el funcionamiento como tu capacidad para explicar el recorrido de una petición. No basta con mostrar un caso exitoso: incluye también entradas inválidas y recursos inexistentes.

## Actividad final de diagnóstico

Para cada situación, indica qué archivo o capa revisarías primero, qué causa sospechas y cómo comprobarías tu hipótesis. No necesitas introducir errores en el proyecto.

| Situación | Pregunta para investigar |
| --- | --- |
| Una ruta no aparece en Swagger | ¿Cómo llega el router a la aplicación? |
| Se aceptan créditos negativos | ¿Dónde se valida el cuerpo de entrada y qué esquema usa la ruta? |
| DELETE responde correctamente, pero el curso sigue apareciendo | ¿Se eliminó el registro y se confirmó la transacción? |
| PUT crea un curso adicional | ¿Se modifica la entidad encontrada o se construye una nueva? |
| La tabla de estudiantes no existe | ¿Se importó el modelo antes de crear las tablas? |
| Los datos parecen desaparecer al reiniciar | ¿Se confirmó la transacción y se usa el mismo archivo SQLite? |
| Un ID inexistente produce `500` | ¿Se controla el resultado de la búsqueda antes de usarlo? |
| Se registran dos cursos con el mismo nombre | ¿Existe una regla que lo prohíba? Si la añadieras, ¿cómo coordinarías servicio y restricción de base de datos? |

Actualmente los nombres de cursos no son únicos. Registrar nombres repetidos no es un fallo del proyecto base; impedirlo requeriría definir una nueva regla.
