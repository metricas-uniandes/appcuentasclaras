from sqlalchemy.sql.elements import and_

from src.modelo.declarative_base import Session, engine, Base
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.modelo.viajeroActividad import ViajeroActividad
from itertools import groupby

class Logica():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.actividades = self.dar_actividades()
        self.gastos = []

    def crear_actividad(self,nombreActividad):
        busqueda = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
        if busqueda is None:
            #FIXME review busqueda
            actividad = Actividad(nombre=nombreActividad.lower())
            actividad.guardar(self.session)
            busqueda = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
            if busqueda is not None:
                return True
            else: 
                return False
        else:
            return False

    def eliminar_actividad(self,nombreActividad):
        actividad = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
        if actividad is not None:
            #FIXME review actividad
            gastos = Gasto.listar_gastos_por_actividad(self.session,actividad.id)
            if len(gastos) > 0:
                return False
            else:
                actividad.eliminar(self.session)
                busqueda = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
                if busqueda is None:
                    self.actividades = self.dar_actividades()
                    return True
                else: 
                    return False
        else:
            return False

    def editar_actividad(self,idActividad,nombreActividad):
        if len(nombreActividad.strip()) >= 1:
            busqueda = Actividad.buscar_actividad_por_nombre_otro_id(self.session,idActividad,nombreActividad)
            #FIXME review busqueda
            if busqueda is not None:
                return False
            else:
                actividad = Actividad.buscar_actividad_por_id(self.session,idActividad)
                actividad.nombre = nombreActividad.lower()
                actividad.guardar(self.session)
                busqueda = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
                if busqueda is not None:
                    self.actividades = self.dar_actividades()
                    return True
                    statusCode = true
                else: 
                    return False
                    statusCode = false
        else:
            return False
            statusCode = false

    def reporte_compensacion(self, nombreActividad):
        actividad = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        viajeros = actividad.viajeros

        if len(viajeros) == 0:
            return []

        gastos = self.dar_gastos(nombreActividad)
        totalGastosActividad = 0
        gastosPorViajero = {}

        cabecera = ['']
        for viajero in viajeros:
            nombreCompleto = viajero.nombre + ' ' + viajero.apellido
            cabecera.append(nombreCompleto)
            gastosPorViajero[nombreCompleto] = 0

        for gasto in gastos:
            totalGastosActividad += gasto["Valor"] 
            nombreViajero = gasto["Nombre"] + " " + gasto["Apellido"]
            gastosPorViajero[nombreViajero] += gasto["Valor"]

        cuotaActividad = totalGastosActividad/len(viajeros)
      
        matriz = [cabecera]
        for i in range(len(viajeros)):
            filaMatriz = []
            nombreFila = viajeros[i].nombre + " " + viajeros[i].apellido
            for j in range(len(viajeros)):
                if viajeros[i] == viajeros[j]:
                    filaMatriz.append(-1)
                    continue

                nombreColumna = viajeros[j].nombre + " " + viajeros[j].apellido
                if gastosPorViajero[nombreFila] >= cuotaActividad:
                    filaMatriz.append(0)
                elif gastosPorViajero[nombreColumna] <= cuotaActividad:
                    filaMatriz.append(0)
                else:
                    diferenciaFila = abs(gastosPorViajero[nombreFila] - cuotaActividad)
                    diferenciaColumna = abs(gastosPorViajero[nombreColumna] - cuotaActividad)
                    if diferenciaColumna >= diferenciaFila:
                        filaMatriz.append(diferenciaFila)
                        gastosPorViajero[nombreColumna] -= diferenciaFila
                        gastosPorViajero[nombreFila] += diferenciaFila
                    else:
                        filaMatriz.append(diferenciaColumna)
                        gastosPorViajero[nombreColumna] -= diferenciaColumna
                        gastosPorViajero[nombreFila] += diferenciaColumna

            filaMatriz.insert(0, nombreFila)
            matriz.append(filaMatriz)

        return matriz
        statusCode = false
    
    def dar_actividades(self):
        actividades = Actividad.listar_actividades(self.session)
        actividadesName = []
        for actividad in actividades:
            actividadesName.append(actividad.nombre)  
        self.actividades = actividadesName     
        return actividadesName
    
    def dar_viajeros(self):
        return []

    def dar_viajeros_actividad_gastos(self, nombreActividad):
        actividad = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        listaViajeros = []
        for viajero in actividad.viajeros:
            listaViajeros.append({"Nombre": viajero.nombre, "Apellido": viajero.apellido})
        return listaViajeros

    def dar_gastos(self, nombreActividad):
        actividad = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
        gastos = Gasto.listar_gastos_por_actividad(self.session,actividad.id)
        gastoList = []
        for gasto in gastos:
            gastoList.append({"Concepto": gasto.concepto,
                              "Fecha": gasto.fecha,
                              "Valor": gasto.valor,
                              "Nombre": gasto.nombre,
                              "Apellido": gasto.apellido})
        self.gastos = gastoList
        self.viajeros = self.dar_viajeros_actividad_gastos(nombreActividad)
        return gastoList

    def crear_viajero(self, nombre, apellido):
        busqueda = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombre, apellido)
        if len(busqueda) == 0:
            viajero = Viajero(nombre=nombre, apellido=apellido)
            viajero.guardar(self.session)
            busqueda = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombre, apellido)
            if len(busqueda) == 0:
                return False
            else:
                return True
        else:
            return False

    def reporte_consolidado_gastos(self):
        gastosList = self.gastos
        resultado = []
        for gasto in self.gastos:
            existe = 0
            for item in resultado:
                if item["Nombre"] == gasto["Nombre"] and item["Apellido"] == gasto["Apellido"]:
                    item["Valor"] += gasto["Valor"]
                    existe += 1
            if existe == 0:                
                resultado.append({"Nombre":gasto["Nombre"], "Apellido":gasto["Apellido"], "Valor":gasto["Valor"]})
        
        for viajero in self.viajeros:
            existe = 0
            for item in resultado:
                if item["Nombre"] == viajero["Nombre"] and item["Apellido"] == viajero["Apellido"]:
                    existe += 1
            if existe == 0:                
                resultado.append({"Nombre":viajero["Nombre"], "Apellido":viajero["Apellido"], "Valor":0})
        return resultado

    def actualizar_viajeros(self, nombreActividad, listaViajeros):
        actividad = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        nuevosViajeros = []
        for viajero in listaViajeros:
            if viajero['Presente']:
                nombreViajero = viajero['Nombre'].split()
                viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero[0], nombreViajero[1])
                nuevosViajeros.append(viajero[0])
        actividad.viajeros = nuevosViajeros
        actividad.guardar(self.session)

    def buscar_actividad_por_nombre(self,nombreActividad):
        actividad = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad) 
        return actividad  

    def buscar_viajero_por_nombre_apellido(self, nombre, apellido):
        return Viajero.buscar_viajero_por_nombre_apellido(self.session, nombre, apellido)
                
    def listar_gastos_por_actividad(self, idActividad):
        return Gasto.listar_gastos_por_actividad(self.session, idActividad)
    
    def listar_gastos_por_viajero_actividad(self, idActividad, idViajero):
        return Gasto.listar_gastos_por_viajero_actvidad(self.session, idActividad, idViajero)

    def dar_viajeros_actividad(self, nombreActividad):
        viajeros = Viajero.listar_viajeros(self.session)
        actividad = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        viajerosActividad = []
        for viajero in viajeros:
            nombreCompleto = viajero.nombre + " " + viajero.apellido
            if actividad.viajero_esta_presente(viajero):
                presente = True
            else:
                presente = False
            viajerosActividad.append({'Nombre': nombreCompleto, 'Presente': presente})
        return viajerosActividad

    def crear_gasto(self, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.agregar_gasto(self.session, concepto, fecha, valor, viajero[0])

    def editar_gasto(self, indice, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.actualizar_gasto(self.session, indice, concepto, fecha, valor, viajero[0])

    def editar_gasto1(self, indice, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.actualizar_gasto(self.session, indice, concepto, fecha, valor, viajero[0])

    def editar_gasto2(self, indice, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.actualizar_gasto(self.session, indice, concepto, fecha, valor, viajero[0])

    def editar_gasto3(self, indice, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.actualizar_gasto(self.session, indice, concepto, fecha, valor, viajero[0])

    def editar_gasto4(self, indice, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.actualizar_gasto(self.session, indice, concepto, fecha, valor, viajero[0])

    def editar_gasto5(self, indice, actividad, concepto, fecha, valor, nombreViajero, apellidoViajero):
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombreViajero, apellidoViajero)
        if len(viajero) == 0:
            return False
        actividad = Actividad.buscar_actividad_por_nombre(self.session, actividad)
        return actividad.actualizar_gasto(self.session, indice, concepto, fecha, valor, viajero[0])
