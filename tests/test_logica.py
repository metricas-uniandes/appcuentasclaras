# -*- coding: utf-8 -*-
from sqlalchemy import and_
from faker import Faker
from src.logica.Logica import Logica
from src.modelo.declarative_base import Session, engine, Base
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero
from src.modelo.gasto import Gasto

import datetime
import unittest

class LogicaTestCase(unittest.TestCase):
    def setUp(self):
        self.logica = Logica()
        self.session = self.logica.session
        self.data_factory = Faker()

    def test_agregar_actividad(self):
        nombre = self.data_factory.word()
        resultado = self.logica.crear_actividad(nombreActividad = nombre)
        self.assertTrue(resultado)

    def test_eliminar_actividad_sin_gastos(self):
        nombre = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad = nombre)
        actividad = Actividad.buscar_actividad_por_nombre(self.session,nombre)
        #Elimininar actividad sin validar gastos
        eliminado = self.logica.eliminar_actividad(nombreActividad = nombre)   
        self.assertTrue(eliminado)

    def test_eliminar_actividad_con_gastos(self):
        # Crear actividad
        nombre = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad = nombre)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session,nombre)
        # Crear viajeros
        cantidadViajeros = self.data_factory.pyint(1, 10)
        cantidadGastos = self.data_factory.pyint(1, 50)
        listaViajerosTest = []
        for x in range(cantidadViajeros):
            nombre = self.data_factory.first_name()
            apellido = self.data_factory.last_name()
            self.logica.crear_viajero(nombre, apellido)
            listaViajerosTest.append(self.logica.buscar_viajero_por_nombre_apellido(nombre, apellido)[0])
        actividad1.viajeros = listaViajerosTest # Asociar viajeros a actividad
        # Escenario 3. La actividad cuenta con n viajeros y con n gastos
        for x in range(cantidadGastos):  # Crear gastos a actividad
            indexViajero = self.data_factory.pyint(0, cantidadViajeros-1)
            viajero = actividad1.viajeros[indexViajero] #viajero al azar
            self._agregar_gasto(concepto = self.data_factory.word()
            ,valor = self.data_factory.pyint(0, 20000)
            ,fecha = datetime.date.today()
            ,idActividad=actividad1.id
            ,idViajero= viajero.id)
        #Elimininar actividad validando gastos
        eliminado = self.logica.eliminar_actividad(nombreActividad = actividad1.nombre)   
        self.assertFalse(eliminado)

    def test_editar_actividad(self):
        nombre = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad = nombre)
        actividad = Actividad.buscar_actividad_por_nombre(self.session,nombre)           
        #Se elimina el nombre de la actividad
        resultado = self.logica.editar_actividad(idActividad=actividad.id,nombreActividad = "")
        self.assertFalse(resultado)
        #Se cambia el nombre de la actividad
        resultado = self.logica.editar_actividad(idActividad=actividad.id,nombreActividad = self.data_factory.word())
        self.assertTrue(resultado)
        #se asigna un nombre de actividad que ya existe
        nombreActividad1 = self.data_factory.word()
        nombreActividad2 = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad = nombreActividad1)
        self.logica.crear_actividad(nombreActividad = nombreActividad2)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad1) 
        actividad2 = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad2) 
        resultado = self.logica.editar_actividad(idActividad=actividad2.id,nombreActividad = actividad1.nombre)
        self.assertFalse(resultado)   


    def test_dar_viajeros_actividad(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        viajeros = self.logica.dar_viajeros_actividad(nombreActividad)
        self.assertEqual([], viajeros)

        nombreViajero = self.data_factory.first_name()
        apellidoViajero = self.data_factory.last_name()
        nombreCompleto = nombreViajero + " " + apellidoViajero
        self.logica.crear_viajero(nombreViajero, apellidoViajero)
        viajeros.append(self.logica.buscar_viajero_por_nombre_apellido(nombreViajero, apellidoViajero))

        viajeros = self.logica.dar_viajeros_actividad(nombreActividad)
        listaEsperada = [{"Nombre": nombreCompleto, "Presente": False}]
        self.assertEqual(listaEsperada, viajeros)

        self.logica.actualizar_viajeros(nombreActividad, [{"Nombre": nombreCompleto, "Presente": True}])
        viajeros = self.logica.dar_viajeros_actividad(nombreActividad)
        listaEsperada = [{"Nombre": nombreCompleto, "Presente": True}]
        self.assertEqual(listaEsperada, viajeros)


    def test_agregar_actividad_repetida(self):
        nombreActividad1= self.data_factory.word()
        resultado1 = self.logica.crear_actividad(nombreActividad = nombreActividad1)
        resultado2 = self.logica.crear_actividad(nombreActividad = nombreActividad1)
        self.assertFalse(resultado2)

    def test_verificar_persistencia_agregar_actividad(self):
        nombre = self.data_factory.word()
        resultado = self.logica.crear_actividad(nombreActividad = nombre)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session,nombre)
        self.assertEqual(actividad1.nombre, nombre)

    def test_reporte_gastos(self):
        # Crear actividad
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
        # Crear viajeros
        cantidadViajeros = self.data_factory.pyint(1, 10)
        cantidadGastos = self.data_factory.pyint(1, 50)
        listaViajerosTest = []
        for x in range(cantidadViajeros):
            nombre = self.data_factory.first_name()
            apellido = self.data_factory.last_name()
            self.logica.crear_viajero(nombre, apellido)
            listaViajerosTest.append(self.logica.buscar_viajero_por_nombre_apellido(nombre, apellido)[0])
        # Escenario 1. La actividad no tiene viajeros asociados
        if len(actividad1.viajeros) == 0:
            self.logica.dar_gastos(nombreActividad)
            reporteGastos = self.logica.reporte_consolidado_gastos()
            self.assertEqual(len(reporteGastos),0)

        actividad1.viajeros = listaViajerosTest # Asociar viajeros a actividad
        # Escenario 2. La actividad tiene viajeros asociados pero no hay gastos generados
        self.logica.dar_gastos(nombreActividad)
        reporteGastos = self.logica.reporte_consolidado_gastos()
        sumaReporteConsolidadoGastos = sum(g["Valor"] for g in reporteGastos)
        self.assertEqual(0,sumaReporteConsolidadoGastos)
        # Escenario 3. La actividad cuenta con n viajeros y con n gastos
        for x in range(cantidadGastos):  # Crear gastos a actividad
            indexViajero = self.data_factory.pyint(0, cantidadViajeros-1)
            viajero = actividad1.viajeros[indexViajero] #viajero al azar
            self._agregar_gasto(concepto = self.data_factory.word()
            ,valor = self.data_factory.pyint(0, 20000)
            ,fecha = datetime.date.today()
            ,idActividad=actividad1.id
            ,idViajero= viajero.id)
            
        self.logica.dar_gastos(nombreActividad)
        reporteGastos = self.logica.reporte_consolidado_gastos()
        # Escenario 3 => Prueba 1: Todos los viajeros de la actividad aparecen en el reporte una sola vez
        for viajero in actividad1.viajeros:
            viajeroEnReporte = 0
            for consolidadoViajero in reporteGastos:
                if consolidadoViajero["Nombre"]==viajero.nombre and consolidadoViajero["Apellido"]==viajero.apellido:
                    viajeroEnReporte += 1
            self.assertEqual(1,viajeroEnReporte)

        # Escenario 3 => Prueba 2: La suma de todos los gastos de la actividad es igual a la suma de la columna "Valor" del reporte consolidado de gastos
        gastosActividad = self.logica.listar_gastos_por_actividad(actividad1.id)
        sumaGastosActividad = sum(ga.valor for ga in gastosActividad)
        sumaReporteConsolidadoGastos = sum(g["Valor"] for g in reporteGastos)
        self.assertEqual(sumaGastosActividad,sumaReporteConsolidadoGastos)
        # Escenario 3 => Prueba 3: La suma de todos los gastos de cada viajero se refleja en la columna Valor del reporte 
        for viajero in actividad1.viajeros:
            listaGastosViajero = self.logica.listar_gastos_por_viajero_actividad(actividad1.id,viajero.id)
            sumaGastosViajero = sum(gv.valor for gv in listaGastosViajero)
            for consolidadoViajero in reporteGastos:
                if consolidadoViajero["Nombre"]==viajero.nombre and consolidadoViajero["Apellido"]==viajero.apellido:
                    self.assertEqual(sumaGastosViajero,consolidadoViajero["Valor"])

    def test_dar_actividades(self):
        consulta1 = self.logica.dar_actividades()
        self.assertEqual(0, len(consulta1))
        self.logica.crear_actividad(nombreActividad = self.data_factory.word())
        self.logica.crear_actividad(nombreActividad = self.data_factory.word())
        consulta2 = self.logica.dar_actividades()
        self.assertEqual(2, len(consulta2))

    def test_asociar_viajero_a_actividad(self):
        nombreActividad, viajero = self._generar_viajero_y_actividad()
        self.logica.crear_viajero(viajero['nombre'], viajero['apellido'])
        viajerosUi = [{'Nombre': viajero['nombreCompleto'], 'Presente': True}]

        self.logica.actualizar_viajeros(nombreActividad, viajerosUi)
        viajerosResultado = self._obtener_viajeros_actividad(nombreActividad)
        self.assertEqual(1, len(viajerosResultado))
        self.assertEqual(viajero['nombre'], viajerosResultado[0].nombre)
        self.assertEqual(viajero['apellido'], viajerosResultado[0].apellido)

    def test_no_asociar_viajero_a_actividad(self):
        nombreActividad, viajero = self._generar_viajero_y_actividad()
        self.logica.crear_viajero(viajero['nombre'], viajero['apellido'])
        viajerosUi = [{'Nombre': viajero['nombreCompleto'], 'Presente': False}]

        self.logica.actualizar_viajeros(nombreActividad, viajerosUi)
        viajerosResultado = self._obtener_viajeros_actividad(nombreActividad)
        self.assertEqual(0, len(viajerosResultado))

    def test_remover_viajero_a_actividad(self):
        nombreActividad, viajero = self._generar_viajero_y_actividad()
        self.logica.crear_viajero(viajero['nombre'], viajero['apellido'])
        viajerosUi = [{'Nombre': viajero['nombreCompleto'], 'Presente': True}]

        self.logica.actualizar_viajeros(nombreActividad, viajerosUi)
        viajerosResultado = self._obtener_viajeros_actividad(nombreActividad)
        self.assertEqual(1, len(viajerosResultado))

        viajerosUi = [{'Nombre': viajero['nombreCompleto'], 'Presente': False}]
        self.logica.actualizar_viajeros(nombreActividad, viajerosUi)

        viajerosResultado = self._obtener_viajeros_actividad(nombreActividad)
        self.assertEqual(0, len(viajerosResultado))

    def _generar_viajero_y_actividad(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        viajero = {"nombre": self.data_factory.first_name(),
                   "apellido": self.data_factory.last_name()
                   }
        viajero["nombreCompleto"] = viajero["nombre"] + " " + viajero["apellido"]
        return nombreActividad, viajero

    def _obtener_viajeros_actividad(self, nombreActividad):
        viajerosResultado = self.session.query(
            Viajero
        ).filter(
            and_(Actividad.nombre == nombreActividad, Actividad.id == Viajero.actividades)
        ).all()
        return viajerosResultado

    def test_dar_gastos(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session,nombreActividad)
        # La actividad no tienen gastos
        consulta1 = self.logica.dar_gastos(actividad1.nombre)
        self.assertEqual(0, len(consulta1))

        cantidadViajeros = self.data_factory.pyint(1, 10)
        cantidadGastos = self.data_factory.pyint(1, 50)
        listaViajerosTest = []
        for x in range(cantidadViajeros):
            nombre = self.data_factory.first_name()
            apellido = self.data_factory.last_name()
            self.logica.crear_viajero(nombre, apellido)
            listaViajerosTest.append(self.logica.buscar_viajero_por_nombre_apellido(nombre, apellido)[0])
        actividad1.viajeros = listaViajerosTest # Asociar viajeros a actividad
        for x in range(cantidadGastos):  # Crear gastos a actividad
            indexViajero = self.data_factory.pyint(0, cantidadViajeros-1)
            viajero = actividad1.viajeros[indexViajero] #viajero al azar
            self._agregar_gasto(concepto = self.data_factory.word()
            ,valor = self.data_factory.pyint(0, 20000)
            ,fecha = datetime.date.today()
            ,idActividad=actividad1.id
            ,idViajero= viajero.id)
        # La actividad tiene gastos
        gastosActividad = self.logica.dar_gastos(actividad1.nombre)
        self.assertEqual(cantidadGastos, len(gastosActividad))

    def test_crear_gasto(self):
        #Crear gasto viajero no existe.
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        nombre = self.data_factory.first_name()
        apellido = self.data_factory.last_name()
        result = self.logica.crear_gasto(actividad=nombreActividad,
                                concepto=self.data_factory.word(),
                                fecha=datetime.date.today(),
                                valor=self.data_factory.pyint(0, 20000),
                                nombreViajero=nombre,
                                apellidoViajero=apellido)

        self.assertEqual(False, result)

        #Crear gasto viajero no agregado a actividad.
        self.logica.crear_viajero(nombre, apellido)
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombre, apellido)
        result = self.logica.crear_gasto(actividad=nombreActividad,
                                concepto=self.data_factory.word(),
                                fecha=datetime.date.today(),
                                valor=self.data_factory.pyint(0, 20000),
                                nombreViajero=nombre,
                                apellidoViajero=apellido)

        self.assertEqual(False, result)

        #Crear gasto.
        actividad1.viajeros = viajero
        actividad1.guardar(self.session)
        result = self.logica.crear_gasto(actividad=nombreActividad,
                                concepto=self.data_factory.word(),
                                fecha=datetime.date.today(),
                                valor=self.data_factory.pyint(0, 20000),
                                nombreViajero=nombre,
                                apellidoViajero=apellido)
        self.assertEqual(True, result)

        #Crear gasto con valor diferente a entero
        result = self.logica.crear_gasto(actividad=nombreActividad,
                                concepto=self.data_factory.word(),
                                fecha=datetime.date.today(),
                                valor=self.data_factory.word(),
                                nombreViajero=nombre,
                                apellidoViajero=apellido)
        self.assertEqual(False, result)

        #Crear gasto con valor 0.
        result = self.logica.crear_gasto(actividad=nombreActividad,
                                concepto='',
                                fecha=datetime.date.today(),
                                valor=self.data_factory.pyint(0, 20000),
                                nombreViajero=nombre,
                                apellidoViajero=apellido)
        self.assertEqual(False, result)

        #Crear gasto sin concepto.
        result = self.logica.crear_gasto(actividad=nombreActividad,
                                concepto=self.data_factory.word(),
                                fecha=datetime.date.today(),
                                valor=0,
                                nombreViajero=nombre,
                                apellidoViajero=apellido)
        self.assertEqual(False, result)

    def test_editar_gasto(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        nombre = self.data_factory.first_name()
        apellido = self.data_factory.last_name()
        self.logica.crear_viajero(nombre, apellido)
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombre, apellido)
        actividad1.viajeros = viajero
        actividad1.guardar(self.session)
        self.logica.crear_gasto(actividad=nombreActividad,
                                concepto=self.data_factory.word(),
                                fecha=datetime.date.today(),
                                valor=self.data_factory.pyint(0, 20000),
                                nombreViajero=nombre,
                                apellidoViajero=apellido)

        gastos = self.logica.dar_gastos(nombreActividad)

        result = self.logica.editar_gasto(indice=0,
                                  actividad=nombreActividad,
                                  concepto=self.data_factory.word(),
                                  fecha=datetime.date.today(),
                                  valor=self.data_factory.pyint(0, 20000),
                                  nombreViajero=nombre,
                                  apellidoViajero=apellido)
        self.assertEqual(True, result)

    def test_dar_viajeros_actividad_gastos(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        nombre = self.data_factory.first_name()
        apellido = self.data_factory.last_name()
        self.logica.crear_viajero(nombre, apellido)
        viajero = Viajero.buscar_viajero_por_nombre_apellido(self.session, nombre, apellido)
        actividad1.viajeros = viajero
        actividad1.guardar(self.session)

        viajerosEnActividad = self.logica.dar_viajeros_actividad_gastos(nombreActividad)
        self.assertEqual(1, len(viajerosEnActividad))
        viajeroEnActividad = viajerosEnActividad[0]
        self.assertEqual(nombre, viajeroEnActividad['Nombre'])
        self.assertEqual(apellido, viajeroEnActividad['Apellido'])


    def test_crear_viajero(self):
        nombreViajero = self.data_factory.first_name()
        apellidoViajero = self.data_factory.last_name()
        self.logica.crear_viajero(nombreViajero, apellidoViajero)

        viajerosModelo = self.session.query(Viajero).first()
        self.assertEqual(nombreViajero, viajerosModelo.nombre)
        self.assertEqual(apellidoViajero, viajerosModelo.apellido)

        result = self.logica.crear_viajero(nombreViajero, apellidoViajero)
        viajerosModelo = self.session.query(Viajero).all()
        self.assertEqual(False, result)
        self.assertEqual(1, len(viajerosModelo))


    def _agregar_gasto(self, concepto, valor, fecha, idActividad, idViajero):
        gasto = Gasto(concepto=concepto, valor=valor, fecha=fecha, actividad = idActividad,  viajero = idViajero)
        self.session.add(gasto)
        self.session.commit()

    def _agregar_viajero_modelo(self, nombre, apellido):
        viajero = Viajero(nombre=nombre,apellido=apellido)
        self.session.add(viajero)
        self.session.commit()
        return viajero

    def tearDown(self):
        '''Consulta todos las actividades'''
        busqueda = self.session.query(Actividad).all()

        '''Borra todas las actividades'''
        for actividad in busqueda:
            self.session.delete(actividad)

        self.session.commit()

        '''Consulta todos los viajeros'''
        busqueda = self.session.query(Viajero).all()

        '''Borra todos los viajeros'''
        for viajero in busqueda:
            self.session.delete(viajero)

        self.session.commit()

        '''Consulta todos los gastos'''
        busqueda = self.session.query(Gasto).all()

        '''Borra todos los gastos'''
        for gasto in busqueda:
            self.session.delete(gasto)

        self.session.commit()
        self.session.close()
