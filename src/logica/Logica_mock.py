'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
class Logica_mock():

    def __init__(self):
        #Este constructor contiene los datos falsos para probar la interfaz
        self.actividades = ["Actividad 1", "Actividad 2", "Actividad 3"]
        self.viajeros = [{"Nombre":"Pepe", "Apellido":"Pérez"}, {"Nombre":"Ana", "Apellido":"Andrade"}]
        self.gastos = [{"Concepto":"Gasto 1", "Fecha": "12-12-2020", "Valor": 10000, "Nombre": "Pepe", "Apellido": "Pérez"}, {"Concepto":"Gasto 2", "Fecha": "12-12-2020", "Valor": 20000, "Nombre":"Ana", "Apellido":"Andrade"}]
        self.matriz = [["", "Pepe Pérez", "Ana Andrade", "Pedro Navajas" ],["Pepe Pérez", -1, 1200, 1000],["Ana Andrade", 0, -1, 1000], ["Pedro Navajas", 0, 0, -1]]
        self.gastos_consolidados = [{"Nombre":"Pepe", "Apellido":"Pérez", "Valor":15000}, {"Nombre":"Ana", "Apellido":"Andrade", "Valor":12000},{"Nombre":"Pedro", "Apellido":"Navajas", "Valor":0}]
        self.viajeros_en_actividad = [{"Nombre": "Pepe Pérez", "Presente":True}, {"Nombre": "Ana Andrade", "Presente":True}, {"Nombre":"Pedro Navajas", "Presente":False}]
