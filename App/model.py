"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf


def newtamplate ():
    template = {
        "digraph" : None,
        "nodigraph" : None,
        "airports" : None
    }
    template["digraph"] = gr.newGraph(datastructure="ADJ_LIST", directed= True, size = 13000, comparefunction = compare)
    template["nodigraph"] = gr.newGraph(datastructure="ADJ_LIST", directed= False, size = 13000, comparefunction = compare)
    template["airports"] = mp.newMap(30000, maptype= "CHAINING", loadfactor= 0.8)
    return(template)

def addairport (template, serv):
    iata = serv["IATA"]
    mp.put(template["airports"], iata, serv)
    addvertice(template, iata)


def addconection(template, serv):
    origen = serv["Departure"]
    destino = serv["Destination"]
    distancia = serv["distance_km"]
    addvertice(template, origen)
    addvertice(template, destino)
    addcon(template, origen, destino, distancia)
    return(template)

def addvertice(template, origen):
    if not gr.containsVertex(template["digraph"], origen):
        gr.insertVertex(template["digraph"], origen)
    return(template)

def addcon(template,origen,destino,distancia):
    edge = gr.getEdge(template['digraph'], origen, destino)
    if edge is None:
        gr.addEdge(template['digraph'],origen,destino, distancia)
    return(template)
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def req1 (template):
    num = gr.vertices(template["digraph"])
    histo = lt.newList("ARRAY_LIST")
    for i in lt.iterator(num):
        j = gr.adjacentEdges(template["digraph"], i)
        o = lt.size(j)
        dicc = {"nombre": i, "numero": o}
        lt.addLast(histo, dicc)
    sa.sort(histo, comaprenums)
    ret = lt.newList("ARRAY_LIST")
    for m in range(1, 6):
        dicctio = lt.getElement(histo, m)
        lt.addLast(ret, mp.get(template["airports"], dicctio["nombre"]))
    return(ret)

def compare(route1, route2):
    """
    Compara dos rutas
    """
    route2 = route2["key"]
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def comaprenums(numero1, numero2):
    numero1 = numero1["numero"]
    numero2 = numero2["numero"]
    if (numero1 == numero2):
        return 0
    elif (numero1 < numero2):
        return 1
    else:
        return -1
