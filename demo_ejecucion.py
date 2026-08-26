import sqlite3

conexion = sqlite3.connect(":memory:")
cursor = conexion.cursor()
cursor.execute("""
    CREATE TABLE jobs(
        job_id VARCHAR(10) PRIMARY KEY,
        job_title VARCHAR(35),
        min_salary INTEGER,
        max_salary INTEGER
    )
""")
conexion.commit()


def crear(job_id, job_title, min_salary, max_salary):
    cursor.execute(
        "INSERT INTO jobs (job_id, job_title, min_salary, max_salary) VALUES (?,?,?,?)",
        [job_id, job_title, min_salary, max_salary],
    )
    conexion.commit()
    print("Puesto creado.")


def leer():
    cursor.execute("SELECT job_id, job_title, min_salary, max_salary FROM jobs")
    for fila in cursor:
        print(fila)


def actualizar(job_id, nuevo_titulo):
    cursor.execute("UPDATE jobs SET job_title = ? WHERE job_id = ?", [nuevo_titulo, job_id])
    conexion.commit()
    print("Puesto actualizado.")


def eliminar(job_id):
    cursor.execute("DELETE FROM jobs WHERE job_id = ?", [job_id])
    conexion.commit()
    print("Puesto eliminado.")


print(">>> 1. Crear")
crear("IT_DBA", "Database Administrator", 4000, 11000)
crear("IT_QA", "QA Analyst", 3500, 8000)

print("\n>>> 2. Leer (todos los puestos)")
leer()

print("\n>>> 3. Actualizar (IT_QA)")
actualizar("IT_QA", "QA Senior Analyst")
leer()

print("\n>>> 4. Eliminar (IT_QA)")
eliminar("IT_QA")

print("\n>>> 2. Leer (después de eliminar)")
leer()

conexion.close()
