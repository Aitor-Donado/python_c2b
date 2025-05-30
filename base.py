from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import date, timedelta

Base = declarative_base()

class LibroDB(Base):
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    codigo_inventario = Column(String, unique=True, nullable=False)
    autor = Column(String)
    isbn = Column(String)
    numero_paginas = Column(Integer)
    disponible = Column(Boolean)

class RevistaDB(Base):
    __tablename__ = 'revistas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    codigo_inventario = Column(String, unique=True, nullable=False)
    numero = Column(String)
    fecha_publicacion = Column(String)
    disponible = Column(Boolean)

class DvdDB(Base):
    __tablename__ = 'dvds'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    codigo_inventario = Column(String, unique=True, nullable=False)
    director = Column(String)
    duracion = Column(Integer)
    disponible = Column(Boolean)

class UsuarioDB(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    id_usuario = Column(String, unique=True, nullable=False)

class PrestamoDB(Base):
    __tablename__ = 'prestamos'

    id = Column(Integer, primary_key=True)
    codigo_inventario = Column(String, ForeignKey('libros.codigo_inventario'))
    id_usuario = Column(String)
    fecha_prestamo = Column(Date, default=date.today)
    fecha_devolucion = Column(Date, default=lambda: date.today() + timedelta(days=14))
    fecha_devolucion_real = Column(Date, nullable=True)

    libro = relationship("LibroDB", backref="prestamos")
# Підключення до SQLite
engine = create_engine('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)

def crear_tablas():
    Base.metadata.create_all(engine)
