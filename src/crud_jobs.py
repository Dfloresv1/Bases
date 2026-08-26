"""
crud_jobs.py
------------------------------------------------------------------
Aplicación de consola en Python que realiza operaciones CRUD
(Create, Read, Update, Delete) sobre la tabla JOBS del esquema HR,
alojado en una base de datos Oracle accedida a través de FreeSQL
(https://freesql.com).

Autor:  <Tu nombre>
Curso:  5K2 - Bases de Datos Avanzadas
Fecha:  Agosto 2026

Requisitos:
    pip install oracledb

La conexión se configura mediante el archivo config.ini (ver
config.ini.example) o mediante variables de entorno, para no dejar
usuario/contraseña escritos directamente en el código fuente.
------------------------------------------------------------------
"""

import configparser
import os
import sys

import oracledb


# --------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA CONEXIÓN
# --------------------------------------------------------------------------
def cargar_configuracion(ruta_config="config.ini"):
    """
    Lee los datos de conexión (usuario, password, dsn) desde config.ini.
    Si el archivo no existe, intenta tomarlos de variables de entorno.
    """
    config = configparser.ConfigParser()

    if os.path.exists(ruta_config):
        config.read(ruta_config)
        db = config["database"]
        return {
            "user": db.get("user"),
            "password": db.get("password"),
            "dsn": db.get("dsn"),
        }

    # Alternativa: variables de entorno (útil para no exponer credenciales)
    return {
        "user": os.environ.get("HR_DB_USER"),
        "password": os.environ.get("HR_DB_PASSWORD"),
        "dsn": os.environ.get("HR_DB_DSN"),
    }


def conectar():
    """
    Crea y devuelve una conexión a la base de datos Oracle usando
    python-oracledb en modo "thin" (no requiere Instant Client).
    """
    cfg = cargar_configuracion()

    if not all([cfg["user"], cfg["password"], cfg["dsn"]]):
        sys.exit(
            "ERROR: faltan datos de conexión. Copia config.ini.example a "
            "config.ini y completa usuario, contraseña y dsn, o define las "
            "variables de entorno HR_DB_USER, HR_DB_PASSWORD y HR_DB_DSN."
        )

    try:
        conexion = oracledb.connect(
            user=cfg["user"], password=cfg["password"], dsn=cfg["dsn"]
        )
        print(f"Conexión exitosa a Oracle (versión cliente thin: {oracledb.__version__})")
        return conexion
    except oracledb.DatabaseError as error:
        sys.exit(f"No fue posible conectar a la base de datos: {error}")


# --------------------------------------------------------------------------
# 2. OPERACIONES CRUD SOBRE HR.JOBS
# --------------------------------------------------------------------------
def crear_job(conexion, job_id, job_title, min_salary, max_salary):
    """CREATE: inserta un nuevo registro en la tabla jobs."""
    sql = """
        INSERT INTO jobs (job_id, job_title, min_salary, max_salary)
        VALUES (:job_id, :job_title, :min_salary, :max_salary)
    """
    with conexion.cursor() as cursor:
        try:
            cursor.execute(
                sql,
                job_id=job_id,
                job_title=job_title,
                min_salary=min_salary,
                max_salary=max_salary,
            )
            conexion.commit()
            print(f"[OK] Puesto '{job_id}' insertado correctamente.")
        except oracledb.IntegrityError:
            print(f"[ERROR] Ya existe un puesto con job_id = '{job_id}'.")
        except oracledb.DatabaseError as error:
            print(f"[ERROR] No se pudo insertar el registro: {error}")


def leer_jobs(conexion, job_id=None):
    """
    READ: muestra todos los registros de jobs, o uno solo si se
    especifica job_id.
    """
    if job_id:
        sql = "SELECT job_id, job_title, min_salary, max_salary FROM jobs WHERE job_id = :job_id"
        parametros = {"job_id": job_id}
    else:
        sql = "SELECT job_id, job_title, min_salary, max_salary FROM jobs ORDER BY job_id"
        parametros = {}

    with conexion.cursor() as cursor:
        cursor.execute(sql, parametros)
        filas = cursor.fetchall()

        if not filas:
            print("No se encontraron registros.")
            return []

        print(f"\n{'JOB_ID':<10}{'JOB_TITLE':<35}{'MIN_SALARY':<12}{'MAX_SALARY':<12}")
        print("-" * 69)
        for fila in filas:
            job_id_, job_title_, min_sal, max_sal = fila
            print(f"{job_id_:<10}{job_title_:<35}{min_sal or 0:<12}{max_sal or 0:<12}")
        print()
        return filas


def actualizar_job(conexion, job_id, job_title=None, min_salary=None, max_salary=None):
    """
    UPDATE: actualiza los campos indicados (no nulos) de un puesto
    existente, identificado por job_id.
    """
    campos = []
    parametros = {"job_id": job_id}

    if job_title is not None:
        campos.append("job_title = :job_title")
        parametros["job_title"] = job_title
    if min_salary is not None:
        campos.append("min_salary = :min_salary")
        parametros["min_salary"] = min_salary
    if max_salary is not None:
        campos.append("max_salary = :max_salary")
        parametros["max_salary"] = max_salary

    if not campos:
        print("[AVISO] No se especificó ningún campo para actualizar.")
        return

    sql = f"UPDATE jobs SET {', '.join(campos)} WHERE job_id = :job_id"

    with conexion.cursor() as cursor:
        cursor.execute(sql, parametros)
        if cursor.rowcount == 0:
            print(f"[AVISO] No existe ningún puesto con job_id = '{job_id}'.")
        else:
            conexion.commit()
            print(f"[OK] Puesto '{job_id}' actualizado correctamente.")


def eliminar_job(conexion, job_id):
    """DELETE: elimina un registro de jobs por su job_id."""
    sql = "DELETE FROM jobs WHERE job_id = :job_id"

    with conexion.cursor() as cursor:
        try:
            cursor.execute(sql, job_id=job_id)
            if cursor.rowcount == 0:
                print(f"[AVISO] No existe ningún puesto con job_id = '{job_id}'.")
            else:
                conexion.commit()
                print(f"[OK] Puesto '{job_id}' eliminado correctamente.")
        except oracledb.IntegrityError:
            # Ocurre si el job_id está siendo usado por employees o job_history
            print(
                f"[ERROR] No se puede eliminar '{job_id}': está referenciado "
                "por empleados o por el historial de puestos (job_history)."
            )


# --------------------------------------------------------------------------
# 3. MENÚ DE CONSOLA
# --------------------------------------------------------------------------
def menu():
    opciones = """
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
"""
    print(opciones)
    return input("Selecciona una opción (1-6): ").strip()


def main():
    conexion = conectar()

    try:
        while True:
            opcion = menu()

            if opcion == "1":
                job_id = input("job_id (máx 10 caracteres): ").strip().upper()
                job_title = input("job_title: ").strip()
                min_salary = input("min_salary: ").strip()
                max_salary = input("max_salary: ").strip()
                crear_job(
                    conexion,
                    job_id,
                    job_title,
                    int(min_salary) if min_salary else None,
                    int(max_salary) if max_salary else None,
                )

            elif opcion == "2":
                leer_jobs(conexion)

            elif opcion == "3":
                job_id = input("job_id a consultar: ").strip().upper()
                leer_jobs(conexion, job_id)

            elif opcion == "4":
                job_id = input("job_id a actualizar: ").strip().upper()
                print("Deja vacío cualquier campo que no quieras modificar.")
                job_title = input("Nuevo job_title: ").strip() or None
                min_salary = input("Nuevo min_salary: ").strip()
                max_salary = input("Nuevo max_salary: ").strip()
                actualizar_job(
                    conexion,
                    job_id,
                    job_title,
                    int(min_salary) if min_salary else None,
                    int(max_salary) if max_salary else None,
                )

            elif opcion == "5":
                job_id = input("job_id a eliminar: ").strip().upper()
                confirmacion = input(f"¿Confirmas eliminar '{job_id}'? (s/n): ").strip().lower()
                if confirmacion == "s":
                    eliminar_job(conexion, job_id)
                else:
                    print("Operación cancelada.")

            elif opcion == "6":
                print("Saliendo de la aplicación...")
                break

            else:
                print("[AVISO] Opción no válida, intenta de nuevo.")

    finally:
        conexion.close()
        print("Conexión cerrada.")


if __name__ == "__main__":
    main()
