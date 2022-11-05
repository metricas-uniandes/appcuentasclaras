from operator import and_

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.viajeroActividad import ViajeroActividad

from src.modelo.declarative_base import Base

class Viajero(Base):
    __tablename__ = 'viajero'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    gasto = relationship('Gasto')    
    actividades = relationship('Actividad', secondary='viajero_actividad')

    def guardar(self, session):
        session.add(self)
        session.commit()

    @staticmethod
    def buscar_viajero_por_nombre_apellido(session, nombre, apellido):
        viajeros = session.query(Viajero).filter(and_(Viajero.nombre == nombre, Viajero.apellido == apellido)).all()
        return viajeros

    @staticmethod
    def listar_viajeros(session):
        viajeros = session.query(Viajero).all()
        return viajeros