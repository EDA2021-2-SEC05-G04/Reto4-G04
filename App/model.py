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
from DISClib.ADT import graph as gr
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dfs
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
    distancia = float(serv["distance_km"])
    addvertice(template, origen)
    addvertice(template, destino)
    addcon(template, origen, destino, distancia)
    return(template)

def addvertice(template, origen):
    if not gr.containsVertex(template["digraph"], origen):
        gr.insertVertex(template["digraph"], origen)
    if not gr.containsVertex(template["nodigraph"], origen):
        gr.insertVertex(template["nodigraph"], origen)
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
def fuertementeConectados(catalog,Aeropuerto1,Aeropuerto2):
    kosa=scc.KosarajuSCC(catalog["digraph"])
    return scc.stronglyConnected(kosa,Aeropuerto1,Aeropuerto2)
def MST(catalog,Salida,millas):
    grafo_nodirigido=catalog["nodigraph"]
    MSTX=prim.edgesMST(grafo_nodirigido,prim.PrimMST(grafo_nodirigido))
    grafo_con_MST=gr.newGraph(directed=False,comparefunction= compare,size=181)
    for i in lt.iterator(MSTX["mst"]):
        if not gr.containsVertex(grafo_con_MST,i["vertexA"]):
            gr.insertVertex(grafo_con_MST,i["vertexA"])
        if not gr.containsVertex(grafo_con_MST,i["vertexB"]):
            gr.insertVertex(grafo_con_MST,i["vertexB"])
        gr.addEdge(grafo_con_MST,i["vertexA"],i["vertexB"],i["weight"])
    RUTA=DFS(grafo_con_MST,Salida)
    visitables=lt.newList("ARRAY_LIST")
    costo_total_MST=0
    for i in lt.iterator(RUTA):
        costo_total_MST+=i["weight"]
    ENkm=millas*1.60
    sobra_falta=""
    if(ENkm>=costo_total_MST*2):
        sobra_falta="Sobraron:"+str((ENkm-costo_total_MST*2)/1.60)+" millas"
    else:
        sobra_falta="Faltaron:"+str((costo_total_MST*2-ENkm)/1.60)+" millas"
    return gr.numVertices(grafo_con_MST),costo_total_MST,RUTA,sobra_falta
    
    

def DFS(graph, source):
    search = {'source': source,
              'visited': None}
    search['visited'] = mp.newMap(numelements=gr.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )
    mp.put(search['visited'], source, {'marked': True, 'edgeTo': None})
    Recorrido=lt.newList("ARRAY_LIST",cmpfunction=comparador_LISTA)
    dfsVertex(search, graph, source,Recorrido)
    return Recorrido
def dfsVertex(search, graph, vertex,Recorrido):
    adjlst = gr.adjacents(graph, vertex)
    for w in lt.iterator(adjlst):
        visited = mp.get(search['visited'], w)
        if visited is None:
            mp.put(search['visited'],
                    w, {'marked': True, 'edgeTo': vertex})
            arco=gr.getEdge(graph,vertex,w)
            lt.addLast(Recorrido,arco)
            dfsVertex(search, graph, w,Recorrido)
def buscar_aero(catalog,aeropuerto):
    return me.getValue(mp.get(catalog["airports"],aeropuerto))
def fueraDeFuncionamiento(catalog,Aeropuerto):
    afectados=lt.newList(cmpfunction=compare2)

    for i in lt.iterator(gr.edges(catalog["digraph"])):
        B=buscar_aero(catalog,i["vertexB"])
        A=buscar_aero(catalog,i["vertexB"])
        if(i["vertexA"] == Aeropuerto and lt.isPresent(afectados,B)==0 and B["IATA"]!=Aeropuerto):
            lt.addLast(afectados,B)
        elif(i["vertexB"]== Aeropuerto and lt.isPresent(afectados,A)==0 and A["IATA"]!=Aeropuerto):
            lt.addLast(afectados,A)
    return afectados
def comparador_LISTA(el1,el2):
    if (el1 == el2):
        return 0
    elif el1 > el2:
        return 1
    else:
        return -1
def compare2(ele1,ele2):
    if (float(ele1["id"]) ==float(ele2["id"])):
        return 0
    elif(float(ele1["id"])>float(ele2["id"])):
        return 1
    else:
        return -1
def loadNODIGRAPH(template):
    dirigido=template["digraph"]
    no_dirigido=template["nodigraph"]
    for i in lt.iterator(gr.edges(dirigido)):
        A=i["vertexA"]
        B=i["vertexB"]
        ida=gr.getEdge(dirigido,B,A)
        ida_X=gr.getEdge(no_dirigido,A,B)
        if(ida!= None and ida_X==None):
            gr.addEdge(no_dirigido,A,B,i["weight"])


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
