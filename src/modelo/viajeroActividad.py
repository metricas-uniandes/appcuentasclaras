from sqlalchemy import Column, Integer, ForeignKey

from src.modelo.declarative_base import Base

class ViajeroActividad(Base):
   __tablename__ = 'viajero_actividad'

   viajero = Column(Integer, ForeignKey('viajero.id'),primary_key=True)
   actividad = Column(Integer, ForeignKey('actividad.id'), primary_key=True)