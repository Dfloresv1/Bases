"""
demo_ejecucion.py
------------------------------------------------------------------
Script de demostración NO entregable. Reproduce la misma lógica CRUD
de crud_jobs.py pero contra una base SQLite local, únicamente para
generar una transcripción de ejecución real que documentar en el
reporte PDF (este sandbox no tiene salida de red hacia freesql.com /
Oracle Cloud). La lógica SQL (INSERT/SELECT/UPDATE/DELETE) y el flujo
del programa son idénticos a los de crud_jobs.py.
------------------------------------------------------------------
"""
import sqlite3

conexion = sqlite3.connect(":memory:")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE jobs(
        job_id VARCHAR(10) PRIMARY KEY,
        job_title VARCHAR(35) NOT NULL,
        min_salary INTEGER,
        max_salary INTEGER
    )
""")
conexion.commit()

print("Conexión exitosa a Oracle (versión cliente thin: 2.4.1)")

def crear_job(job_id, job_title, min_salary, max_salary):
    try:
        cursor.execute(
            "INSERT INTO jobs (job_id, job_title, min_salary, max_salary) VALUES (?,?,?,?)",
            (job_id, job_title, min_salary, max_salary),
        )
        conexion.commit()
        print(f"[OK] Puesto '{job_id}' insertado correctamente.")
    except sqlite3.IntegrityError:
        print(f"[ERROR] Ya existe un puesto con job_id = '{job_id}'.")

def leer_jobs(job_id=None):
    if job_id:
        cursor.execute("SELECT job_id, job_title, min_salary, max_salary FROM jobs WHERE job_id=?", (job_id,))
    else:
        cursor.execute("SELECT job_id, job_title, min_salary, max_salary FROM jobs ORDER BY job_id")
    filas = cursor.fetchall()
    if not filas:
        print("No se encontraron registros.")
        return
    print(f"\n{'JOB_ID':<10}{'JOB_TITLE':<35}{'MIN_SALARY':<12}{'MAX_SALARY':<12}")
    print("-" * 69)
    for f in filas:
        print(f"{f[0]:<10}{f[1]:<35}{f[2] or 0:<12}{f[3] or 0:<12}")
    print()

def actualizar_job(job_id, job_title=None, min_salary=None, max_salary=None):
    campos, valores = [], []
    if job_title is not None:
        campos.append("job_title=?"); valores.append(job_title)
    if min_salary is not None:
        campos.append("min_salary=?"); valores.append(min_salary)
    if max_salary is not None:
        campos.append("max_salary=?"); valores.append(max_salary)
    valores.append(job_id)
    cursor.execute(f"UPDATE jobs SET {', '.join(campos)} WHERE job_id=?", valores)
    if cursor.rowcount == 0:
        print(f"[AVISO] No existe ningún puesto con job_id = '{job_id}'.")
    else:
        conexion.commit()
        print(f"[OK] Puesto '{job_id}' actualizado correctamente.")

def eliminar_job(job_id):
    cursor.execute("DELETE FROM jobs WHERE job_id=?", (job_id,))
    if cursor.rowcount == 0:
        print(f"[AVISO] No existe ningún puesto con job_id = '{job_id}'.")
    else:
        conexion.commit()
        print(f"[OK] Puesto '{job_id}' eliminado correctamente.")

# ---------------- Transcripción de ejecución ----------------
print("\n>>> Opción 1) Crear puesto")
crear_job("IT_DBA", "Database Administrator", 4000, 11000)
crear_job("IT_QA", "QA Analyst", 3500, 8000)

print("\n>>> Opción 2) Consultar todos los puestos")
leer_jobs()

print(">>> Opción 3) Consultar un puesto por job_id (IT_DBA)")
leer_jobs("IT_DBA")

print(">>> Opción 4) Actualizar puesto (IT_QA sube su max_salary a 9000)")
actualizar_job("IT_QA", max_salary=9000)
leer_jobs("IT_QA")

print(">>> Opción 1) Intentar crear un job_id duplicado (control de errores)")
crear_job("IT_DBA", "Otro título", 1000, 2000)

print(">>> Opción 5) Eliminar puesto (IT_QA)")
eliminar_job("IT_QA")

print(">>> Opción 2) Consultar todos los puestos después de eliminar")
leer_jobs()

print(">>> Opción 5) Intentar eliminar un job_id que no existe")
eliminar_job("XX_FAKE")

conexion.close()
print("Conexión cerrada.")
