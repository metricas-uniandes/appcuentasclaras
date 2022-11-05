from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from operator import and_
from src.modelo.viajero import Viajero
from src.modelo.declarative_base import Base

class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column(Integer, primary_key=True)
    concepto = Column(String)
    valor = Column(Integer)
    fecha = Column(String)
    actividad = Column(Integer, ForeignKey('actividad.id'))
    viajero = Column(Integer, ForeignKey('viajero.id'))

    @staticmethod
    def listar_gastos_por_actividad(session,idActividad):
        busqueda = session.query(Gasto.valor,
                    Gasto.viajero,
                    Gasto.concepto,
                    Gasto.fecha,
                    Viajero.nombre,
                    Viajero.apellido
        ).filter(Gasto.actividad == idActividad
        ).join(Viajero
        ).filter(Viajero.id == Gasto.viajero
        ).all()
        return busqueda

    @staticmethod
    def listar_gastos_por_viajero_actvidad(session,idActividad,idViajero):
        busqueda = session.query(Gasto).filter(and_(Gasto.actividad == idActividad, Gasto.viajero == idViajero)).all()
        return busqueda
    
          