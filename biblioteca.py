from datetime import date, timedelta

from base import LibroDB, RevistaDB, DvdDB, UsuarioDB, PrestamoDB, crear_tablas, Session
from clases import Libro, Revista, DVD, Usuario
from helpers import (
    libro_a_db, db_a_libro,
    revista_a_db, db_a_revista,
    dvd_a_db, db_a_dvd,
    usuario_a_db, db_a_usuario
)

# === Libro ===
def agregar_libro():
    print("\n== Agregar Libro ==")
    titulo = input("Título: ")
    codigo = input("Código de inventario: ")
    autor = input("Autor: ")
    isbn = input("ISBN: ")
    paginas = int(input("Número de páginas: "))

    libro = Libro(titulo, codigo, autor, isbn, paginas)
    libro_db = libro_a_db(libro)

    with Session() as session:
        session.add(libro_db)
        session.commit()
    print("✅ Libro guardado.")

def mostrar_libros():
    print("\n== Lista de Libros ==")
    with Session() as session:
        libros_db = session.query(LibroDB).all()
        for ldb in libros_db:
            db_a_libro(ldb).mostrar_info()

# === Revista ===
def agregar_revista():
    print("\n== Agregar Revista ==")
    titulo = input("Título: ")
    codigo = input("Código de inventario: ")
    numero = input("Número de edición: ")
    fecha = input("Fecha de publicación (YYYY-MM-DD): ")

    revista = Revista(titulo, codigo, numero, fecha)
    revista_db = revista_a_db(revista)

    with Session() as session:
        session.add(revista_db)
        session.commit()
    print("✅ Revista guardada.")

def mostrar_revistas():
    print("\n== Lista de Revistas ==")
    with Session() as session:
        revistas_db = session.query(RevistaDB).all()
        for rdb in revistas_db:
            db_a_revista(rdb).mostrar_info()

# === DVD ===
def agregar_dvd():
    print("\n== Agregar DVD ==")
    titulo = input("Título: ")
    codigo = input("Código de inventario: ")
    director = input("Director: ")
    duracion = int(input("Duración (minutos): "))

    dvd = DVD(titulo, codigo, director, duracion)
    dvd_db = dvd_a_db(dvd)

    with Session() as session:
        session.add(dvd_db)
        session.commit()
    print("✅ DVD guardado.")

def mostrar_dvds():
    print("\n== Lista de DVDs ==")
    with Session() as session:
        dvds_db = session.query(DvdDB).all()
        for ddb in dvds_db:
            db_a_dvd(ddb).mostrar_info()

# === Usuario ===
def agregar_usuario():
    print("\n== Agregar Usuario ==")
    nombre = input("Nombre: ")
    id_usuario = input("ID de usuario: ")

    usuario = Usuario(nombre, id_usuario)
    usuario_db = usuario_a_db(usuario)

    with Session() as session:
        session.add(usuario_db)
        session.commit()
    print("✅ Usuario guardado.")

def mostrar_usuarios():
    print("\n== Lista de Usuarios ==")
    with Session() as session:
        usuarios_db = session.query(UsuarioDB).all()
        for udb in usuarios_db:
            db_a_usuario(udb)
            print(f"{udb.id_usuario} - {udb.nombre}")

def prestar_material():
    codigo = input("Código del material a prestar: ")
    id_usuario = input("ID del usuario: ")

    with Session() as session:
        # Шукаємо книгу
        material_db = session.query(LibroDB).filter_by(codigo_inventario=codigo).first()
        tipo_material = "Libro"

        # Якщо не знайшли книгу, шукаємо журнал
        if not material_db:
            material_db = session.query(RevistaDB).filter_by(codigo_inventario=codigo).first()
            tipo_material = "Revista"

        # Якщо не знайшли журнал, шукаємо DVD
        if not material_db:
            material_db = session.query(DvdDB).filter_by(codigo_inventario=codigo).first()
            tipo_material = "DVD"

        if not material_db:
            print("❌ Material no encontrado.")
            return

        if not material_db.disponible:
            print("⚠️ El material no está disponible.")
            return

        # Створення позики
        prestamo = PrestamoDB(
            codigo_inventario=material_db.codigo_inventario,
            id_usuario=id_usuario,
            fecha_prestamo=date.today(),
            fecha_devolucion=date.today() + timedelta(days=14)
        )
        session.add(prestamo)

        # Оновлення статусу матеріалу
        material_db.disponible = False
        session.commit()

        print(f"✅ {tipo_material} prestado hasta {prestamo.fecha_devolucion}")

def eliminar_material():
    print("\n== Eliminar Material ==")
    codigo = input("Código del material a eliminar: ")

    with Session() as session:
        material = (
            session.query(LibroDB).filter_by(codigo_inventario=codigo).first()
            or session.query(RevistaDB).filter_by(codigo_inventario=codigo).first()
            or session.query(DvdDB).filter_by(codigo_inventario=codigo).first()
        )

        if not material:
            print("❌ Material no encontrado.")
            return

        session.delete(material)
        session.commit()
        print("✅ Material eliminado correctamente.")

def editar_material():
    print("\n== Editar Material ==")
    codigo = input("Código del material a editar: ")

    with Session() as session:
        libro = session.query(LibroDB).filter_by(codigo_inventario=codigo).first()
        if libro:
            print(f"📘 Editando Libro: {libro.titulo}")
            libro.titulo = input(f"Título [{libro.titulo}]: ") or libro.titulo
            libro.autor = input(f"Autor [{libro.autor}]: ") or libro.autor
            libro.isbn = input(f"ISBN [{libro.isbn}]: ") or libro.isbn
            paginas = input(f"Número de páginas [{libro.paginas}]: ")
            libro.paginas = int(paginas) if paginas else libro.paginas

        else:
            revista = session.query(RevistaDB).filter_by(codigo_inventario=codigo).first()
            if revista:
                print(f"📰 Editando Revista: {revista.titulo}")
                revista.titulo = input(f"Título [{revista.titulo}]: ") or revista.titulo
                revista.numero = input(f"Número [{revista.numero}]: ") or revista.numero
                fecha = input(f"Fecha de publicación [{revista.fecha_publicacion}]: ")
                revista.fecha_publicacion = fecha or revista.fecha_publicacion

            else:
                dvd = session.query(DvdDB).filter_by(codigo_inventario=codigo).first()
                if dvd:
                    print(f"💿 Editando DVD: {dvd.titulo}")
                    dvd.titulo = input(f"Título [{dvd.titulo}]: ") or dvd.titulo
                    dvd.director = input(f"Director [{dvd.director}]: ") or dvd.director
                    duracion = input(f"Duración (min) [{dvd.duracion}]: ")
                    dvd.duracion = int(duracion) if duracion else dvd.duracion
                else:
                    print("❌ Material no encontrado.")
                    return

        session.commit()
        print("✅ Cambios guardados correctamente.")


def mostrar_todos_los_materiales():
    with Session() as session:
        print("\n📚 == Libros ==")
        for libro in session.query(LibroDB).all():
            print(f"📘 [{libro.codigo_inventario}] {libro.titulo} — {libro.autor}  | Disponible: {'Si' if libro.disponible else 'No'}")

        print("\n📰 == Revistas ==")
        for revista in session.query(RevistaDB).all():
            print(f"🗞️ [{revista.codigo_inventario}] {revista.titulo} — №{revista.numero} | Disponible: {'Si' if revista.disponible else 'No'}")

        print("\n💿 == DVD ==")
        for dvd in session.query(DvdDB).all():
            print(f"💽 [{dvd.codigo_inventario}] {dvd.titulo} — {dvd.director}  | Disponible: {'Si' if dvd.disponible else 'No'}")

def devolver_material():
    print("\n== Devolver Material ==")
    codigo = input("Código del material: ")
    id_usuario = input("ID del usuario: ")

    with Session() as session:
        # Шукаємо останній активний (не повернутий) запис про позику
        prestamo = (
            session.query(PrestamoDB)
            .filter_by(codigo_inventario=codigo, id_usuario=id_usuario)
            .filter(PrestamoDB.fecha_devolucion_real.is_(None))  # не повернений
            .first()
        )

        if not prestamo:
            print("❌ No se encontró préstamo activo para este material y usuario.")
            return

        # Повертаємо матеріал00
        prestamo.fecha_devolucion_real = date.today()

        # Оновлюємо статус у відповідній таблиці
        material = (
            session.query(LibroDB).filter_by(codigo_inventario=codigo).first()
            or session.query(RevistaDB).filter_by(codigo_inventario=codigo).first()
            or session.query(DvdDB).filter_by(codigo_inventario=codigo).first()
        )

        if material:
            material.disponible = True

        session.commit()
        print("✅ Material devuelto correctamente.")
def historial_prestamos():
    print("\n== Historial de Préstamos ==")
    with Session() as session:
        prestamos = session.query(PrestamoDB).all()
        for p in prestamos:
            devuelto = p.fecha_devolucion_real or "⏳ No devuelto"
            print(f"📚 {p.codigo_inventario} | 👤 {p.id_usuario} | 📅 {p.fecha_prestamo} → {p.fecha_devolucion} | 🔄 {devuelto}")

# === Menú principal ===
def menu():
    crear_tablas()
    while True:
        print("\n==== Menú principal ====")
        print("1. Agregar libro")
        print("2. Mostrar libros")
        print("3. Agregar revista")
        print("4. Mostrar revistas")
        print("5. Agregar DVD")
        print("6. Mostrar DVDs")
        print("7. Agregar usuario")
        print("8. Mostrar usuarios")
        print("9. Prestar material")
        print("10. Mostrar estado de todos los materiales")
        print("11. Devolver material")
        print("12. Historial de préstamos")
        print("13. Editar material")
        print("14. Eliminar material")
        print("0. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            mostrar_libros()
        elif opcion == "3":
            agregar_revista()
        elif opcion == "4":
            mostrar_revistas()
        elif opcion == "5":
            agregar_dvd()
        elif opcion == "6":
            mostrar_dvds()
        elif opcion == "7":
            agregar_usuario()
        elif opcion == "8":
            mostrar_usuarios()
        elif opcion == "9":
            prestar_material()
        elif opcion == "10":
            mostrar_todos_los_materiales()  
        elif opcion == "11":
           devolver_material()
        elif opcion == "12":
            historial_prestamos()
        elif opcion == "13":
            editar_material()
        elif opcion == "14":
            eliminar_material()
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    menu()
