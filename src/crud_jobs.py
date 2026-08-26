import oracledb

# Datos de conexión a FreeSQL / Oracle
usuario = "TU_USUARIO"
password = "TU_PASSWORD"
dsn = "TU_DSN"

conexion = oracledb.connect(user=usuario, password=password, dsn=dsn)
cursor = conexion.cursor()


def crear():
    job_id = input("job_id: ")
    job_title = input("job_title: ")
    min_salary = input("min_salary: ")
    max_salary = input("max_salary: ")

    cursor.execute(
        "INSERT INTO jobs (job_id, job_title, min_salary, max_salary) "
        "VALUES (:1, :2, :3, :4)",
        [job_id, job_title, min_salary, max_salary],
    )
    conexion.commit()
    print("Puesto creado.")


def leer():
    cursor.execute("SELECT job_id, job_title, min_salary, max_salary FROM jobs")
    for fila in cursor:
        print(fila)


def actualizar():
    job_id = input("job_id a actualizar: ")
    nuevo_titulo = input("Nuevo job_title: ")

    cursor.execute(
        "UPDATE jobs SET job_title = :1 WHERE job_id = :2",
        [nuevo_titulo, job_id],
    )
    conexion.commit()
    print("Puesto actualizado.")


def eliminar():
    job_id = input("job_id a eliminar: ")
    cursor.execute("DELETE FROM jobs WHERE job_id = :1", [job_id])
    conexion.commit()
    print("Puesto eliminado.")


while True:
    print("\n1. Crear\n2. Leer\n3. Actualizar\n4. Eliminar\n5. Salir")
    opcion = input("Opción: ")

    if opcion == "1":
        crear()
    elif opcion == "2":
        leer()
    elif opcion == "3":
        actualizar()
    elif opcion == "4":
        eliminar()
    elif opcion == "5":
        break

conexion.close()
