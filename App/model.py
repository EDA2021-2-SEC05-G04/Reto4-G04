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

from math import radians, cos, sin, asin, sqrt
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
assert cf

def analizer( ):
    analyzer = {
                    'components': None,
                    'paths': None
                    }
    return(analyzer)

def newtamplate ():
    template = {
        "digraph" : None,
        "nodigraph" : None,
        "airports" : None,
        "latitude" : None,
        "city" : None
    }

    template["latitude"] = om.newMap("BST")
    template["digraph"] = gr.newGraph(datastructure="ADJ_LIST", directed= True, size = 13000, comparefunction = compare)
    template["nodigraph"] = gr.newGraph(datastructure="ADJ_LIST", directed= False, size = 13000, comparefunction = compare)
    template["airports"] = mp.newMap(30000, maptype= "CHAINING", loadfactor= 0.8)
    template["city"] = mp.newMap(30000, maptype= "CHAINING", loadfactor= 0.8)
    return(template)

def addcity(template, ciudad):
    nombre = ciudad["city"]

    mp.put(template["city"], nombre, ciudad)
def addairport (template, serv):
    iata = serv["IATA"]
    latitude = serv["Latitude"]
    longitude = serv["Longitude"]
    dicc = {"longitud": longitude, "serv": serv}
    mp.put(template["airports"], iata, serv)
    om.put(template["latitude"], float(latitude), dicc)
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

def req3(template, ciudad1, ciudad2,analyzer):
    u1 = findair(template, ciudad1)
    u2 = findair(template, ciudad2)
    partida = findmin(u1)
    llegada = findmin(u2)
    connectedComponents(template , analyzer)
    minimumCostPaths(analyzer, template,partida)
    camino = minimumCostPath(analyzer, llegada)
    return(camino) 

def findmin (u):
    longiciu = float(u[2])
    laticiu = float(u[1])
    selec = None
    min = None
    for i in lt.iterator(u[0]):
        longiaer = float(i["value"]["longitud"])
        latiaer = float(i["key"])
        dis = haversine(longiciu, laticiu, longiaer, latiaer)
        if min == None:
            min = dis
            selec = i["value"]["serv"]
        elif ( min < dis):
            min = dis
            selec = i["value"]["serv"]
    return(selec["IATA"])


    
def findair(template, ciudad):
    city = mp.get(template["city"], ciudad)
    latitud = float(city["value"]["lat"])
    longitud = float(city["value"]["lng"])
    aeropuerto = lt.newList("ARRAY_LIST")
    
    lati = om.keys(template["latitude"], latitud - 10, latitud  + 10)
    if lati != None:
        for i in lt.iterator(lati):
            dato = om.get(template["latitude"], i)
            if (float(dato["value"]["longitud"]) > longitud - 10) and (float(dato["value"]["longitud"]) < longitud + 10):
    
                lt.addLast(aeropuerto, dato)
               
                
    return(aeropuerto, latitud , longitud )
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
def connectedComponents(template , analyzer):
    analyzer['components'] = scc.KosarajuSCC(template['digraph'])
    return scc.connectedComponents(analyzer['components'])

def minimumCostPaths(analyzer, template,partida):
    analyzer['paths'] = djk.Dijkstra(template['digraph'], partida)
    return analyzer
def minimumCostPath(analyzer, destino):
    path = djk.pathTo(analyzer['paths'], destino)
    return path

def hasPath(analyzer, destino):
    return djk.hasPathTo(analyzer['paths'], destino)
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

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r