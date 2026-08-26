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
    ├── crud_jobs.py          # Código fuente de la aplicación
    └── config.ini.example    # Plantilla de configuración de conexión
```

## Requisitos

- Python 3.9 o superior
- Una cuenta activa en [FreeSQL](https://freesql.com) con el esquema `HR`
  disponible (o tu propio usuario con permisos sobre una tabla `jobs`)
- Librería `oracledb` (driver oficial de Oracle para Python, no requiere
  instalar Oracle Instant Client gracias a su modo "thin")

## Instalación

```bash
git clone <url-del-repositorio>
cd proyecto_crud_jobs
pip install -r requirements.txt
```

## Configuración de la conexión

1. Copia el archivo de ejemplo:
   ```bash
   cp src/config.ini.example src/config.ini
   ```
2. Edita `src/config.ini` con tus credenciales:
   ```ini
   [database]
   user = TU_USUARIO
   password = TU_PASSWORD
   dsn = TU_DSN_O_CONNECT_STRING
   ```
3. El `dsn` se obtiene desde el panel de conexión de FreeSQL, o si tu
   instancia corre sobre Oracle Autonomous Database, desde **DB Connection
   > Connection Strings** en la consola de Oracle Cloud.

> ⚠️ `config.ini` está en `.gitignore`: nunca subas tus credenciales reales
> al repositorio. Solo se versiona `config.ini.example`.

## Ejecución

```bash
cd src
python crud_jobs.py
```

Verás un menú interactivo:

```
==================================================
   CRUD - Tabla JOBS (Esquema HR - Oracle/FreeSQL)
==================================================
 1) Crear puesto (Create)
 2) Consultar todos los puestos (Read)
 3) Consultar un puesto por job_id (Read)
 4) Actualizar puesto (Update)
 5) Eliminar puesto (Delete)
 6) Salir
--------------------------------------------------
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

Ver `reporte_actividad.pdf` para la explicación detallada del código,
capturas/ejemplos de ejecución y conclusiones de la actividad.

## Autor

Curso: 5K2 - Bases de Datos Avanzadas
