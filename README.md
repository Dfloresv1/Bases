# CRUD en Python para la tabla JOBS (Oracle HR / FreeSQL)

Aplicación de consola en Python que realiza operaciones **CRUD** (Create,
Read, Update, Delete) sobre la tabla `JOBS` del esquema `HR`, en una base de
datos Oracle accedida a través de la herramienta [FreeSQL](https://freesql.com).

## Contenido del repositorio

```
proyecto_crud_jobs/
├── README.md
├── requirements.txt
├── reporte_actividad.pdf     # Documentación del código y de la ejecución
└── src/
    └── crud_jobs.py          # Código fuente de la aplicación
```

## Requisitos

- Python 3.9 o superior
- Una cuenta activa en [FreeSQL](https://freesql.com) con el esquema `HR`
  disponible
- Librería `oracledb`

## Instalación

```bash
git clone <url-del-repositorio>
cd proyecto_crud_jobs
pip install -r requirements.txt
```

## Configuración de la conexión

Abre `src/crud_jobs.py` y edita estas tres líneas al inicio del archivo con
tus datos de FreeSQL:

```python
usuario = "TU_USUARIO"
password = "TU_PASSWORD"
dsn = "TU_DSN"
```

El `dsn` se obtiene desde el panel de conexión de tu Worksheet en FreeSQL.

## Ejecución

```bash
cd src
python crud_jobs.py
```

Menú disponible:

```
1. Crear
2. Leer
3. Actualizar
4. Eliminar
5. Salir
```

## Estructura de la tabla JOBS

```sql
CREATE TABLE jobs(
  job_id VARCHAR2(10),
  job_title VARCHAR2(35) CONSTRAINT job_title_nn NOT NULL,
  min_salary NUMBER(6),
  max_salary NUMBER(6),
  CONSTRAINT job_id_pk PRIMARY KEY(job_id)
);
```

## Documentación completa

Ver `reporte_actividad.pdf` para la explicación del código y ejemplos de
ejecución.

## Autor

Curso: 5K2 - Bases de Datos Avanzadas
