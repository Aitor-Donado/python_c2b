from clases import Libro, Revista, DVD, Usuario, Prestamo
from base import LibroDB, RevistaDB, DvdDB, UsuarioDB, PrestamoDB

# ==== Libro ====
def libro_a_db(libro):
    return LibroDB(
        titulo=libro.titulo,
        codigo_inventario=libro.codigo_inventario,
        autor=libro.autor,
        isbn=libro.isbn,
        numero_paginas=libro.numero_paginas,
        disponible=libro.disponible
    )

def db_a_libro(libro_db):
    libro = Libro(
        titulo=libro_db.titulo,
        codigo_inventario=libro_db.codigo_inventario,
        autor=libro_db.autor,
        isbn=libro_db.isbn,
        numero_paginas=libro_db.numero_paginas
    )
    libro.disponible = libro_db.disponible
    return libro

# ==== Revista ====
def revista_a_db(revista):
    return RevistaDB(
        titulo=revista.titulo,
        codigo_inventario=revista.codigo_inventario,
        numero=revista.numero,
        fecha_publicacion=revista.fecha_publicacion,
        disponible=revista.disponible
    )

def db_a_revista(revista_db):
    revista = Revista(
        titulo=revista_db.titulo,
        codigo_inventario=revista_db.codigo_inventario,
        numero=revista_db.numero,
        fecha_publicacion=revista_db.fecha_publicacion
    )
    revista.disponible = revista_db.disponible
    return revista

# ==== DVD ====
def dvd_a_db(dvd):
    return DvdDB(
        titulo=dvd.titulo,
        codigo_inventario=dvd.codigo_inventario,
        director=dvd.director,
        duracion=dvd.duracion,
        disponible=dvd.disponible
    )

def db_a_dvd(dvd_db):
    dvd = DVD(
        titulo=dvd_db.titulo,
        codigo_inventario=dvd_db.codigo_inventario,
        director=dvd_db.director,
        duracion=dvd_db.duracion
    )
    dvd.disponible = dvd_db.disponible
    return dvd

# ==== Usuario ====
def usuario_a_db(usuario):
    return UsuarioDB(
        nombre=usuario.nombre,
        id_usuario=usuario.id_usuario
    )

def db_a_usuario(usuario_db):
    return Usuario(
        nombre=usuario_db.nombre,
        id_usuario=usuario_db.id_usuario
    )

# ==== Prestamo ====
def prestamo_a_db(prestamo):
    return PrestamoDB(
        codigo_inventario=prestamo.material.codigo_inventario,
        id_usuario=prestamo.usuario.id_usuario,
        fecha_prestamo=prestamo.fecha_prestamo,
        fecha_devolucion=prestamo.fecha_devolucion
    )

# Примітка: db_a_prestamo потребує доступу до material та usuario з бази — реалізуємо пізніше.
