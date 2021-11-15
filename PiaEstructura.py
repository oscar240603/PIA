from collections import namedtuple
import csv
import datetime
import os
import sqlite3
import sys
from sqlite3 import Error
cantidades = [] #Esta lista vacia, guardara las cantidades totales de los articulos para despues sumarlas 
v = [] #Esta lista vacia, guardara los datos de la namedtuple para despues hacerles busqueda especifica
diccionario = {}#Este diccionario guardara el folio como clave y dentro de el vendra una variable que tenga guardada la tupla nominada
fecha_actual = datetime.datetime.now()
fecha_sistema = datetime.datetime.strftime(fecha_actual, '%B %d %Y %H:%M:%S')
ventas = namedtuple('ventas', 'folio,desc_articulo, cantidad, precio,fechaconversion')
try:
    with sqlite3.connect('Articulos.db') as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Venta (Folio INTEGER PRIMARY KEY);')
        c.execute('CREATE TABLE IF NOT EXISTS Articulo (Descripcion TEXT NOT NULL, Cantidad REAL, Precio REAL, Fecha TEXT NOT NULL, Total REAL, Venta INTEGER NOT NULL, FOREIGN KEY(Venta) REFERENCES Venta(Folio));')
    while True:
        print('')
        print(' ***** MENU ***** ')
        print('Registrar una venta[1]')
        print('Consultar una venta[2]')
        print('Reporte de ventas para una fecha especifica[3]')
        print('Salir[4]')
        op = input('Introduzca la opcion: ')
        print('*'*50)
        if op == '1':
            while True: 
                try:
                    folio = int(input('Introduzca el folio: '))
                    fecha = input('Introduzca fecha de la venta d/m/y: ')
                    fechaconversion = datetime.datetime.strptime(fecha, '%d/%m/%Y' )
                    if folio in diccionario.keys(): #si el 'folio' que ingreso ya esta registrado que intente con otro
                        print('Este folio ya esta registrado, intento con otro: ')
                    else:
                        while True: #si no, ejecutar este ciclo
                            while True:
                                desc_articulo = input('Describa el articulo: ')
                                if desc_articulo == '' :
                                     False
                                     print('*'*50)
                                     print('Este campo es obligatorio')
                                     print('*'*50)
                                else:
                                    while True:
                                        cantidad = int(input('Cantidad de piezas vendidas: '))
                                        if cantidad<0:
                                            False
                                            print('*'*50)
                                            print("No se admiten valores negativos")
                                            print('*'*50)
                                        else:
                                            break
                                    while True:
                                         precio = int(input('Precio de venta c/u $: '))
                                         if precio<0:
                                           False
                                           print('*'*50)
                                           print("No se admiten valores negativos")
                                           print('*'*50)
                                         else:
                                            datos = ventas(folio,desc_articulo,cantidad,precio,fechaconversion)#Esta variable guardara los datos de la tupla nominada 
                                            diccionario[folio,fechaconversion] = datos
                                            total = precio * cantidad
                                            cantidades.append(total)
                                            v.append(datos)
                                            break
                                agregar = input('Desea seguir agregando [S/N]: ')
                                if agregar == 'N':#si 'agregar' es igual a 'N', imprimir la suma total de los articulos
                                        print('Registro agregado exitosamente')
                                        iva = sum(cantidades) * .16
                                        total_iva = sum(cantidades) + iva
                                        print('*'*50)
                                        print(f'El monto sin iva es: ${sum(cantidades)}')
                                        print(f'Desglose de iva(16%): ${iva} ')
                                        print(f'Total a pagar con iva: ${total_iva}')
                                        print('*'*50)
                                        print('')
                                        print(f'Fecha actual: {fecha_sistema}')
                                        try:
                                          with sqlite3.connect('Articulos.db') as conn:
                                            c = conn.cursor()
                                            c.execute("INSERT INTO Venta VALUES(?)",(folio,))
                                            for elemento in v:
                                                if folio == elemento.folio:
                                                    c.execute("INSERT INTO Articulo VALUES(?,?,?,?,?,?)",(elemento.desc_articulo,elemento.cantidad,elemento.precio,fecha,total_iva,folio))
                                        except Error as e:
                                            print(e)
                                        except Exception:
                                            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
                                        finally:
                                              if conn:
                                                 conn.close()
                                                 break
                                        with open('ventas.csv','w',newline='') as archivo:
                                            grabador = csv.writer(archivo)
                                            grabador.writerow(('folio','desc_articulo','cantidad','precio'))
                                            grabador.writerows([(folio, datos.desc_articulo, datos.cantidad, datos.precio) for folio, datos in diccionario.items()])
                                            print(f'\ngrabado exitoso en {os.getcwd()}')           
                            break
                        break
                except ValueError:
                    print("Introduza Un dato valido")
                    False       
        elif op == '2':
            busqueda = int(input('Introduzca el folio a buscar: '))
            for elemento in v: #Por cada elemento de la lista 'v' 
                if busqueda == elemento.folio: #si 'busqueda' es igual al folio que esta en la lista, entonces imprime los siguiente: 
                    print('*'*50)
                    print(f'Descripcion del articulo(s): {elemento.desc_articulo} ')
                    print(f'Cantidad de piezas vendidass: {elemento.cantidad} ')
                    print(f'Precio de cada una: {elemento.precio} ')
            print('*'*50)
            print(f'Desglose de iva(16%): ${iva}')
            print(f'Gran total ${total_iva}')
            print('*'*50)
        elif op == '3':
            busq_fecha = input('Introduzca la fecha de la venta a buscar: ')
            busq_conversion = datetime.datetime.strptime(busq_fecha, '%d/%m/%Y' )
            if busq_conversion > fecha_actual:
                    print('*' * 50)
                    print('Fecha no valida')
                    print('*' * 50)
            if busq_conversion == elemento.fechaconversion: #si 'busq_fecha' es igual a la fecha que esta en la lista, entonces imprime lo siguiente
                for elemento in v:
                    if  busq_conversion == elemento.fechaconversion:
                        print(f'Descripcion del articulo(s): {elemento.desc_articulo}' )
                print(f'Desglose de iva(16%): ${iva}')
                print(f'Gran total ${total_iva}')
            else:
                print('*' * 50)
                print('Esa fecha no tiene ventas')
                print('*' * 50)
        elif op == '4':
            break
except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
finally:
    if conn:
        conn.close()