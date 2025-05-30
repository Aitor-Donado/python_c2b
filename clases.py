# clases.py

class Material:
    def __init__(self, titulo, codigo_inventario):
        self.titulo = titulo
        self.codigo_inventario = codigo_inventario
        self.disponible = True

    def mostrar_info(self):
        print(f"Título: {self.titulo}")
        print(f"Código de inventario: {self.codigo_inventario}")
        print(f"Disponible: {'Sí' if self.disponible else 'No'}")

class Libro(Material):
    def __init__(self, titulo, codigo_inventario, autor, isbn, numero_paginas):
        super().__init__(titulo, codigo_inventario)
        self.autor = autor
        self.isbn = isbn
        self.numero_paginas = numero_paginas

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Autor: {self.autor}")
        print(f"ISBN: {self.isbn}")
        print(f"Número de páginas: {self.numero_paginas}")

class Revista(Material):
    def __init__(self, titulo, codigo_inventario, numero, fecha_publicacion):
        super().__init__(titulo, codigo_inventario)
        self.numero = numero
        self.fecha_publicacion = fecha_publicacion

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Número: {self.numero}")
        print(f"Fecha de publicación: {self.fecha_publicacion}")

class DVD(Material):
    def __init__(self, titulo, codigo_inventario, director, duracion):
        super().__init__(titulo, codigo_inventario)
        self.director = director
        self.duracion = duracion

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Director: {self.director}")
        print(f"Duración: {self.duracion} minutos")

class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario

class Prestamo:
    def __init__(self, material, usuario, fecha_prestamo, fecha_devolucion=None):
        self.material = material
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

class GestorBiblioteca:
    def __init__(self):
        self.materiales = []
        self.usuarios = []
        self.prestamos = []

    def agregar_material(self, material):
        self.materiales.append(material)

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def prestar_material(self, codigo_inventario, id_usuario, fecha_prestamo):
        material = next((m for m in self.materiales if m.codigo_inventario == codigo_inventario and m.disponible), None)
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        if material and usuario:
            material.disponible = False
            prestamo = Prestamo(material, usuario, fecha_prestamo)
            self.prestamos.append(prestamo)
            print("Material prestado correctamente.")
        else:
            print("Material no disponible o usuario no encontrado.")

    def devolver_material(self, codigo_inventario, fecha_devolucion):
        prestamo = next((p for p in self.prestamos if p.material.codigo_inventario == codigo_inventario and not p.fecha_devolucion), None)
        if prestamo:
            prestamo.fecha_devolucion = fecha_devolucion
            prestamo.material.disponible = True
            print("Material devuelto correctamente.")
        else:
            print("Préstamo no encontrado.")

    def buscar_material(self, codigo_inventario):
        material = next((m for m in self.materiales if m.codigo_inventario == codigo_inventario), None)
        if material:
            material.mostrar_info()
        else:
            print("Material no encontrado.")