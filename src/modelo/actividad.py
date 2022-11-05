from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy import desc
from operator import and_
from src.modelo.declarative_base import Base
from src.modelo.gasto import Gasto
from src.modelo.viajeroActividad import ViajeroActividad
from src.modelo.viajero import Viajero

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    gastos = relationship('Gasto', cascade='all, delete, delete-orphan')
    viajeros = relationship('Viajero', secondary='viajero_actividad')

    def guardar(self, session):
        session.add(self)
        session.commit()

    def eliminar(self, session):
        session.delete(self)
        session.commit()

    @staticmethod
    def buscar_actividad_por_nombre_otro_id(session,idActividad,nombre):
        busqueda = session.query(Actividad).filter(and_(Actividad.id != idActividad, Actividad.nombre == nombre.lower())).first()
        return busqueda

    @staticmethod
    def buscar_actividad_por_nombre(session,nombre):
        busqueda = session.query(Actividad).filter_by(nombre=nombre.lower()).first()
        return busqueda
    
    @staticmethod
    def buscar_actividad_por_id(session,idActividad):
        busqueda = session.query(Actividad).filter_by(id=idActividad).first()
        return busqueda

    @staticmethod
    def listar_actividades(session):
        return session.query(Actividad).all()
    
    def viajero_esta_presente(self, viajero):
        if viajero in self.viajeros:
            return True
        else:
            return False

    def agregar_gasto(self, session, concepto, fecha, valor, viajero):
        if viajero not in self.viajeros:
            return False

        if not self.validar_datos_gasto(valor, concepto):
            return False

        gasto = Gasto(concepto=concepto, valor=valor, fecha=fecha,
                      actividad=self.id,  viajero=viajero.id)
        session.add(gasto)
        session.commit()
        return True

    def actualizar_gasto(self, session, indice, concepto, fecha, valor, viajero):
        if viajero not in self.viajeros:
            return False

        if not self.validar_datos_gasto(valor, concepto):
            return False

        gasto = self.gastos[indice]
        gasto.concepto = concepto
        gasto.fecha = fecha
        gasto.valor = valor
        gasto.viajero = viajero.id
        session.add(gasto)
        session.commit()
        return True

    def validar_datos_gasto(self, valor, concepto):
        if valor == 0:
            return False
        if concepto == '':
            return False
        try:
            int(valor)
        except ValueError:
            return False

        return True
