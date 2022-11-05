import datetime
import unittest

from faker import Faker

from src.logica.Logica import Logica
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero


class ReporteCompensacionTestCase(unittest.TestCase):
    def setUp(self):
        self.logica = Logica()
        self.session = self.logica.session
        self.data_factory = Faker()
        self.nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(self.nombreActividad)
        Actividad.buscar_actividad_por_nombre(self.session, self.nombreActividad)

    def test_reporte_sin_viajeros(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)
        cantidadViajeros = 3
        listaViajerosTest = self._crear_viajeros_aleatorios(cantidadViajeros)
        matriz = self.logica.reporte_compensacion(actividad1.nombre)
        self.assertEqual(0, len(matriz))

    def test_reporte_viajeros_sin_gastos(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)

        cantidadViajeros = 3
        listaViajerosTest = self._crear_viajeros_aleatorios(cantidadViajeros)

        actividad1.viajeros = [listaViajerosTest[0], listaViajerosTest[1], listaViajerosTest[2]]
        actividad1.guardar(self.session)
        matriz = self.logica.reporte_compensacion(nombreActividad)
        matrizEsperada = [["",
                           listaViajerosTest[0].nombre + " " + listaViajerosTest[0].apellido,
                           listaViajerosTest[1].nombre + " " + listaViajerosTest[1].apellido,
                           listaViajerosTest[2].nombre + " " + listaViajerosTest[2].apellido
                           ],
                          [listaViajerosTest[0].nombre + " " + listaViajerosTest[0].apellido, -1, 0, 0],
                          [listaViajerosTest[1].nombre + " " + listaViajerosTest[1].apellido, 0, -1, 0],
                          [listaViajerosTest[2].nombre + " " + listaViajerosTest[2].apellido, 0, 0, -1]]

        self.assertEqual(matrizEsperada, matriz)

    def test_reporte_con_gastos(self):
        nombreActividad = self.data_factory.word()
        self.logica.crear_actividad(nombreActividad)
        actividad1 = Actividad.buscar_actividad_por_nombre(self.session, nombreActividad)

        cantidadViajeros = 4
        listaViajerosTest = self._crear_viajeros_aleatorios(cantidadViajeros)

        actividad1.viajeros = listaViajerosTest
        actividad1.guardar(self.session)
        gasto1 = Gasto(concepto=self.data_factory.word(),
                      valor=400,
                      fecha=datetime.date.today(),
                      actividad=actividad1.id,
                      viajero=listaViajerosTest[0].id)
        self.session.add(gasto1)

        gasto2 = Gasto(concepto=self.data_factory.word(),
                      valor=200,
                      fecha=datetime.date.today(),
                      actividad=actividad1.id,
                      viajero=listaViajerosTest[0].id)
        self.session.add(gasto2)

        gasto3 = Gasto(concepto=self.data_factory.word(),
                      valor=100,
                      fecha=datetime.date.today(),
                      actividad=actividad1.id,
                      viajero=listaViajerosTest[1].id)
        self.session.add(gasto3)

        gasto4 = Gasto(concepto=self.data_factory.word(),
                      valor=700,
                      fecha=datetime.date.today(),
                      actividad=actividad1.id,
                      viajero=listaViajerosTest[2].id)
        self.session.add(gasto4)

        gasto5 = Gasto(concepto=self.data_factory.word(),
                      valor=200,
                      fecha=datetime.date.today(),
                      actividad=actividad1.id,
                      viajero=listaViajerosTest[3].id)
        self.session.add(gasto5)
        self.session.commit()

        matriz = self.logica.reporte_compensacion(nombreActividad)
        nombresViajeros = [viajeroTest.nombre + " " + viajeroTest.apellido for viajeroTest in listaViajerosTest]
        self.assertEqual([""] + nombresViajeros, matriz[0])

        columnaMatriz = [fila[0] for fila in matriz]
        self.assertEqual([""] + nombresViajeros, columnaMatriz)

        contenidoMatriz = matriz[1:]
        contenidoMatriz = [contenido[1:] for contenido in contenidoMatriz]
        matrizEsperada = [[-1, 0, 0, 0],
                          [200, -1, 100, 0],
                          [0, 0, -1, 0],
                          [0, 0, 200, -1]]

        self.assertEqual(matrizEsperada, contenidoMatriz)

    def _crear_viajeros_aleatorios(self, cantidadViajeros):
        listaViajerosTest = []
        for x in range(cantidadViajeros):
            nombre = self.data_factory.first_name()
            apellido = self.data_factory.last_name()
            self.logica.crear_viajero(nombre, apellido)
            listaViajerosTest.append(self.logica.buscar_viajero_por_nombre_apellido(nombre, apellido)[0])
        return listaViajerosTest

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