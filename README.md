# API Académica

API educativa para administrar cursos y estudiantes con **FastAPI, SQLModel y SQLite**. El código incluye comentarios en español para estudiar cómo se conectan las rutas HTTP, la validación de datos y la persistencia.

La explicación detallada del proyecto, la práctica con Swagger y los ejercicios están en la [guía para estudiantes](docs.md). Las pruebas documentadas están en [entrega-pruebas/informe-pruebas.md](entrega-pruebas/informe-pruebas.md).

## Funcionalidades implementadas

- CRUD completo de cursos: crear, listar, consultar, actualizar y eliminar.
- Crear y consultar estudiantes (listado y búsqueda por ID).
- Validar los datos de entrada y responder con códigos HTTP adecuados (`200`, `201`, `404`, `422`).
- Conservar los registros en una base de datos SQLite local (`database.db`) con tablas `course` y `student`.

## Tecnologías

| Herramienta | Uso |
| --- | --- |
| FastAPI | Aplicación web, rutas y documentación interactiva. |
| Uvicorn | Servidor que ejecuta la API. |
| SQLModel | Modelos de tablas y operaciones de base de datos. |
| Pydantic | Esquemas y validación de datos. |
| SQLite | Almacenamiento en el archivo `database.db`. |

Las versiones utilizadas están en [requirements.txt](requirements.txt). El proyecto se ha ejecutado con **Python 3.12**.

## Inicio rápido

Abre una terminal en la carpeta del proyecto, donde está `main.py`.

### 1. Crear y activar el entorno virtual

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si el entorno `venv` ya existe, basta con activarlo.

### 2. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Ejecutar la API

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

`main:app` identifica el objeto `app` del archivo `main.py`. La opción `--reload` recarga el servidor cuando editas el código durante el desarrollo. Para detenerlo, presiona `Ctrl+C`.

Abre la [documentación interactiva Swagger](http://127.0.0.1:8000/docs) para probar los endpoints con **Try it out → Execute**.

La base de datos y sus tablas se crean al iniciar la aplicación. Ejecuta el comando desde la raíz del proyecto para usar siempre el mismo archivo `database.db`.

## Endpoints disponibles

### Courses

| Método | Ruta | Operación | Estado de éxito |
| --- | --- | --- | --- |
| `POST` | `/courses` | Crear un curso. | `201` |
| `GET` | `/courses` | Listar todos los cursos. | `200` |
| `GET` | `/courses/{course_id}` | Consultar un curso por ID. | `200` |
| `PUT` | `/courses/{course_id}` | Actualizar un curso (completo). | `200` |
| `DELETE` | `/courses/{course_id}` | Eliminar un curso. | `200` |

### Students

| Método | Ruta | Operación | Estado de éxito |
| --- | --- | --- | --- |
| `POST` | `/students` | Crear un estudiante. | `201` |
| `GET` | `/students` | Listar todos los estudiantes. | `200` |
| `GET` | `/students/{student_id}` | Consultar un estudiante por ID. | `200` |

Un recurso inexistente devuelve `404`. Los datos que incumplen el esquema o un ID no entero en la ruta devuelven `422`. La ruta `/` no está definida; utiliza `/docs`, `/courses` o `/students`.

## Ejemplos de uso

### Crear un curso

```json
{
  "name": "Programación I",
  "credits": 3,
  "active": true
}
```

### Actualizar un curso (`PUT`)

Los tres campos son obligatorios:

```json
{
  "name": "Programación II",
  "credits": 4,
  "active": false
}
```

### Eliminar un curso

`DELETE /courses/{course_id}` responde:

```json
{
  "message": "Course deleted"
}
```

### Crear un estudiante

```json
{
  "name": "Ana Pérez",
  "email": "ana@universidad.edu",
  "semester": 4
}
```

Si se omite `active`, el valor predeterminado es `true`.

## Reglas de entrada

### Course (crear)

| Campo | Regla |
| --- | --- |
| `name` | Obligatorio; entre 3 y 80 caracteres. |
| `credits` | Obligatorio; entero entre 1 y 6. |
| `active` | Opcional; booleano con valor predeterminado `true`. |

### Course (actualizar con `CourseUpdate`)

| Campo | Regla |
| --- | --- |
| `name` | Obligatorio; entre 3 y 80 caracteres. |
| `credits` | Obligatorio; entero entre 1 y 6. |
| `active` | Obligatorio; booleano sin valor predeterminado. |

### Student (crear)

| Campo | Regla |
| --- | --- |
| `name` | Obligatorio; entre 3 y 80 caracteres. |
| `email` | Obligatorio; texto no vacío. |
| `semester` | Obligatorio; entero entre 1 y 10. |
| `active` | Opcional; booleano con valor predeterminado `true`. |

## Estructura del proyecto

```text
api_acad-mica/
├── main.py                       # Aplicación y ciclo de vida
├── database/database.py          # Motor SQLite y sesiones
├── models/
│   ├── course.py                 # Modelo de la tabla de cursos
│   └── student.py                # Modelo de la tabla de estudiantes
├── schemas/
│   ├── course.py                 # CourseCreate, CourseUpdate, CourseResponse
│   └── student.py                # StudentCreate, StudentResponse
├── routers/
│   ├── courses.py                # Endpoints HTTP de cursos
│   └── students.py               # Endpoints HTTP de estudiantes
├── services/
│   ├── course_service.py         # Lógica de cursos
│   └── student_service.py        # Lógica de estudiantes
├── entrega-pruebas/
│   ├── informe-pruebas.md        # Informe de pruebas
│   └── evidencias/               # Capturas de Swagger
├── requirements.txt
├── docs.md
├── ejercicio.md
└── README.md
```

El flujo principal es: **petición HTTP → router y validación → servicio → base de datos → respuesta JSON**.

Ambos recursos comparten la misma conexión SQLite (`database.db`) con tablas distintas.

Para seguir el código paso a paso, comprender `Depends`, `Session`, `commit()` y `refresh()`, o resolver problemas de ejecución, consulta [docs.md](docs.md).
