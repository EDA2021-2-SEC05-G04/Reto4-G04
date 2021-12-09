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
 """

import config as cf
import model
import csv

def newtemplate():
    return(model.newtamplate())
def initanalizer ():
    a = model.analizer()
    return(a)
def loaddata(template):
    servicesfile = cf.data_dir + "routes-utf8-small.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.addconection(template, service)
def loadcity(template):
    servicesfile = cf.data_dir + "worldcities-utf8.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.addcity(template, service)

def loadNODIGRAPH(template):
    return model.loadNODIGRAPH(template)
def loadair(template):
    servicesfile = cf.data_dir + "airports-utf8-small.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for service in input_file:
        model.addairport(template,service)

def req1(template):
    i = model.req1(template)
    return(i)
def fuertementeConectados(catalog,Aeropuerto1,Aeropuerto2):
    return model.fuertementeConectados(catalog,Aeropuerto1,Aeropuerto2)
def MST(catalog,Salida,millas):
    return model.MST(catalog,Salida,millas)
def fueraDeFuncionamiento(catalog,Aeropuerto):
    return model.fueraDeFuncionamiento(catalog,Aeropuerto)
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
