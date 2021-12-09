"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import model
import controller
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
assert cf
from prettytable import PrettyTable
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Requerimiento 1 (Grupal): Encontrar puntos de interconexión aérea")
    print("3-Requerimiento 2 (Grupal): Encontrar clústeres de tráfico aéreo")
    print("5-Requerimiento 4 (Grupal): Utilizar las millas de viajero")
    print("6-Requerimiento 5 (Grupal): Cuantificar el efecto de un aeropuerto cerrado")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        template = controller.newtemplate()
        a = controller.loaddata(template)
        controller.loadair(template)
        controller.loadcity(template)
        analyzer = controller.initanalizer()
        controller.loadNODIGRAPH(template)
        print(gr.numVertices(template["digraph"]))
        print(gr.numEdges(template["digraph"]))
    elif int(inputs[0]) == 2:
        masv = controller.req1(template)
        print(masv)
    elif int(inputs[0]) == 3:
        partida = input("ingrese ciudad de partida")
        llegada = input("ingrese ciudad de llgadad")
        path = model.req3(template,partida,llegada,analyzer)
        print(path)
        pass
    elif int(inputs[0]) == 4:
        Aeropuerto1=input("Aeropuerto 1 IATA:")
        Aeropuerto2=input("Aeropuerto 2 IATA:")
        print(Aeropuerto1+" y "+Aeropuerto2,"¿Están fuertemente conectados?---",controller.fuertementeConectados(template,Aeropuerto1,Aeropuerto2))
    elif int(inputs[0]) == 5:
        Salida=input("Aeropuerto IATA:")
        Millas=float(input("Digite las millas:"))
        vertices,costo_total_MST,RUTA,sobra_falta=controller.MST(template,Salida,Millas)
        table=PrettyTable()
        print("La cantidad de nodos conectados en el árbol de recubrimiento es:",vertices)
        print("El costo del MST partiendo desde :",Salida,"es:",costo_total_MST,"kilómetros")
        table.field_names=["Departure","Destination","distance_km"]
        for i in lt.iterator(RUTA):
            table.add_row([i["vertexA"],i["vertexB"],i["weight"]])
        print(table)
        print(sobra_falta)
    elif int(inputs[0]) == 6:
        Aeropuerto=input("Escriba el aeropuerto:")
        lista_afectados=controller.fueraDeFuncionamiento(template,Aeropuerto)
        table=PrettyTable()
        table.field_names=["IATA","NAME","CITY","COUNTRY"]
        print("Hay una cantidad de",lt.size(lista_afectados),"aeropuertos afectados.")
        print("Primeros 3 y últimos 3")
        for i in range(1,4):
            element=lt.getElement(lista_afectados,i)
            table.add_row([element["IATA"],element["Name"],element["City"],element["Country"]])
        for i in range(lt.size(lista_afectados)-2,lt.size(lista_afectados)+1):
            element=lt.getElement(lista_afectados,i)
            table.add_row([element["IATA"],element["Name"],element["City"],element["Country"]])
        print(table)
    else:
        sys.exit(0)
sys.exit(0)
