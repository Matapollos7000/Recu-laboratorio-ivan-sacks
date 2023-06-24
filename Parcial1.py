
from datetime import datetime
import json
import re
import csv
from functools import reduce
import random

def parser_csv(path:str)->list:
    """Recibe un archivo.csv, guarda los datos en una lista de diccionarios
    y retorna esa lista """
    lista_personajes = []
    archivo = open(path,newline='',encoding='utf-8')
    for line in archivo: 
        personajes = {};
        datos = re.sub(r"\r","",line)
        datos = re.sub(r"\$\%"," ",datos)
        datos = re.sub(r"Three-","Three ",datos)
        datos = re.sub(r"Shin-","Shin ",datos)
        datos = re.split(",|\n", datos)      
        personajes["ID"] = int(datos[0])
        personajes["Nombre"] = str(datos[1])
        personajes["Raza"] = str(datos[2])
        personajes["Poder de pelea"] = int(datos[3])
        personajes["Poder de ataque"] = int(datos[4])
        personajes["Habilidades"] = str(datos[5])
        lista_personajes.append(personajes)
    archivo.close()
    return lista_personajes
    
lista_personajes = parser_csv("parcial1\DBZ.csv")

###2
def cantidad_raza(clave,lista):
    """Recibe una clave y una lista de diccionarios,
    cuenta cuatos personajes de cada tipo de raza hay y lo imprime"""
    contador_raza = {}
    for raza in lista:
        if raza[clave] not in contador_raza:
            contador_raza[raza[clave]] = 1
        else:
            contador_raza[raza[clave]] += 1
    for raza, cantidad in contador_raza.items():   
        print(f"Hay {cantidad} {raza}")

###3
def presonajes_raza(lista, clave, segunda_clave, tercera_clave):
    """Recive una lista y tres claves. Luego busca y separa los personajes con razas mixtas para luego
    imprimirlos en cada una de las dos razas mientras se imprime los nombres de los personajes con sus 
    respectivas razas"""
    contador_raza = {"Razas":[]}
    razas_mixtas = {"Saiyan":[], "Androide": []}
    for raza in lista:
        if raza[clave] not in contador_raza["Razas"]:
            if re.search("-", raza["Raza"]):
                if re.search("e-", raza["Raza"]):
                    androide = (f"\t{raza[segunda_clave]} | {tercera_clave}: {raza[tercera_clave]}")
                    razas_mixtas["Androide"].append(androide)
                else:
                    saiyan = (f"\t{raza[segunda_clave]} | {tercera_clave}: {raza[tercera_clave]}")
                    razas_mixtas["Saiyan"].append(saiyan)
            else:
                contador_raza["Razas"].append(raza[clave])
    pos = 0
    bandera = [0,0,0]
    for raza in contador_raza["Razas"]:
        print(f"{contador_raza['Razas'][pos]}")     
        for raza in lista:
            if contador_raza['Razas'][pos] == raza["Raza"]:
                print(f"\t{raza[segunda_clave]} | {tercera_clave}: {raza[tercera_clave]}")
                if contador_raza['Razas'][pos] == "Humano" and bandera[0] == 0:
                    for clave in range(len(razas_mixtas["Androide"])):        
                        print(razas_mixtas["Androide"][clave])
                    for clave in range(len(razas_mixtas["Saiyan"])):  
                        print(razas_mixtas["Saiyan"][clave])                   
                    bandera[0] = 1
                if contador_raza['Razas'][pos] == "Androide" and bandera[1] == 0:
                    for clave in range(len(razas_mixtas["Androide"])):        
                        print(razas_mixtas["Androide"][clave])                
                    bandera[1] = 1
                if contador_raza['Razas'][pos] == "Saiyan" and bandera[2] == 0:
                    for clave in range(len(razas_mixtas["Saiyan"])):  
                        print(razas_mixtas["Saiyan"][clave])   
                    bandera[2] = 1
        pos += 1

###4
def personajes_habilidad(clave, lista):
    """Recibe una clave y una lista, le pide al usuario que ingrese una habilidad y le muestra 
    las coincidencias"""
    habilidad_buscada = input("Ingresa la habilidad a buscar ")
    coincidencias = 0
    for raza in lista:
        if habilidad_buscada in raza[clave]:
            promedio_poder = int((raza["Poder de ataque"] + raza["Poder de pelea"])/2)
            print(f" {raza['Nombre']}, Raza: {raza['Raza']}, Poder = {promedio_poder} \n") 
            coincidencias = 1
    if coincidencias == 0:
        print("La habilidad que has ingesado es incorrecta o no existe")
        
##5
def jugar_batalla(lista):
    """Recibe una lista, el jugador elige un personaje y la maquina otro, el que tenga más
    ataque gana y se guardan los datos de la batalla en un archivo.txt creado en el momento"""
    personajes = 0
    jugadores = {"Maquina": [], "Usuario": []}
    for raza in lista:
        print(f"{raza['ID']}, {raza['Nombre']} \n")
    jugador = int(input("Ingrese el ID correspondiente al personaje a jugar "))

    for raza in lista:
        if jugador == raza["ID"]:
            jugador = raza["Nombre"] 
            ataque = raza["Poder de ataque"]
            jugadores["Usuario"].append(jugador)
            jugadores["Usuario"].append(ataque)
        personajes += 1

    personajes = random.randint(0, personajes)
    jugador_maquina = lista[personajes]["Nombre"] 
    ataque_maquina = lista[personajes]["Poder de ataque"]
    jugadores["Maquina"].append(jugador_maquina)
    jugadores["Maquina"].append(ataque_maquina)

    if jugadores["Usuario"][1] > jugadores["Maquina"][1]:
        ganador = jugadores["Usuario"][0]
        perdedor = jugadores["Maquina"][0]
    else:
        ganador = jugadores["Maquina"][0]
        perdedor = jugadores["Usuario"][0]

    fecha_actual = datetime.now()
    nombre_archivo = r"parcial1\batallas.txt"
    with open(nombre_archivo, "a") as archivo:
        archivo.write(f"{fecha_actual.strftime(r'%Y-%m-%d %H:%M:%S')}, Ganador: {ganador}, Perdedor: {perdedor}\n")
    archivo.close()

##6
def guardar_json(lista, raza, habilidad):
    """Recive una lista y dos valores, busca sus coincidencias en la lista, 
    guarda las coincidencias con sus respectivos personajes en un .json """
    personajes_filtrados = []
    for personaje in lista:
        if personaje["Raza"] == raza:
            habilidades_filtradas = []
            for hab in personaje["Habilidades"]:
                if habilidad not in hab:
                    habilidades_filtradas.append(hab)
            habilidades_filtradas = "".join(habilidades_filtradas)
            personaje_filtrado = {
                "Nombre": personaje["Nombre"],
                "Poder de ataque": personaje["Poder de ataque"],
                "Habilidades": habilidades_filtradas
            }
            personajes_filtrados.append(personaje_filtrado)

    nombre_archivo = f"parcial1\{raza}_{habilidad}.json"

    with open(nombre_archivo, "w",encoding = 'utf-8') as archivo:
        json.dump(personajes_filtrados, archivo, ensure_ascii = False, indent = 4)

    print(f"Se han guardado {len(personajes_filtrados)} personajes en el archivo {nombre_archivo}.") 

    return nombre_archivo

##7
def leer_jason(nombre_archivo):
    """Recibe un .json y se lo muestra al usuario"""
    with open(nombre_archivo, "r", encoding = "utf-8") as archivo:
        personajes = json.load(archivo)
        
    for personaje in personajes:
        print(f"Nombre: {personaje['Nombre']} - Poder de ataque: {personaje['Poder de ataque']} - Habilidades: {personaje['Habilidades']} \n")

##Extra
def buffear_saiyan(lista, clave):
    """Recibe una lista y una clave, aumenta los valores de ataque de los saiyan y les da una nueva habilidad,
    luego guarda todos los personajes modificados en un .csv y retorna el archivo"""
    saiyajines_modificados = []
    for raza in lista:
        if "Saiyan" in raza[clave]:
            raza["Poder de pelea"] = int(raza["Poder de pelea"] * 1.5)
            raza["Poder de ataque"] = int(raza["Poder de ataque"] * 1.7)
            raza["Habilidades"] = (f"{raza['Habilidades']} | transformación nivel dios")
            saiyajines = {
                "Nombre": raza['Nombre'],
                "Poder de pelea": raza['Poder de pelea'],
                "Poder de ataque": raza['Poder de ataque'],
                "Habilidades": raza['Habilidades']
            }
            saiyajines_modificados.append(saiyajines)

    nombre_archivo = f"parcial1\Saiyans_modificados.csv"

    with open(nombre_archivo, "w", newline='', encoding = 'utf-8') as archivo_csv:
        writer = csv.DictWriter(archivo_csv, delimiter='-', fieldnames = saiyajines_modificados[0].keys())
        writer.writeheader()
        writer.writerows(saiyajines_modificados)

        print(f"Se han guardado {len(saiyajines_modificados)} saiyans en {nombre_archivo}.") 

    return nombre_archivo

##A
def ordenar_personajes_por_atributo(lista, atributo, orden):
    """Recibe una lista, una clave e un booleano,
    los ordena y devuelve la lista"""
    if orden == True:
        for i in range(len(lista) -1):
            for j in range(i +1, len(lista)):
                if((lista[i])[atributo] > lista[j][atributo]):
                    lista[i], lista[j] = lista[j], lista[i]
    if orden == False:
        for i in range(len(lista) -1):
            for j in range(i +1, len(lista)):
                if((lista[i])[atributo] < lista[j][atributo]):
                    lista[i], lista[j] = lista[j], lista[i]
    return lista

##B
def generar_codigo_personaje(personaje):
    """Recibe un personaje, compara diferentes valores y guarda el más grande , lo identa
    con su respectivo nombre e id y lo retorna  """
    nombre = personaje["Nombre"]
    primer_letra = nombre[0]
    valor_maximo = max(personaje["Poder de pelea"], personaje["Poder de ataque"])

    if personaje["Poder de pelea"] == personaje["Poder de ataque"] :
        ganador = "AD"
    elif personaje["Poder de pelea"] > personaje["Poder de ataque"]:
        ganador = "A" 
    else:
        ganador = "D"

    if ganador == "AD":
        id_personaje = str(personaje["ID"]).zfill(8)
    else:
        id_personaje = str(personaje["ID"]).zfill(9)

    lista_codigo = map(str, [primer_letra, '-', ganador, '-', str(valor_maximo).zfill(4), '-', id_personaje])
    codigo_personaje = reduce(lambda acum, valor: acum + valor, lista_codigo)

    return codigo_personaje[:18] 

##C
def agregar_codigos_personajes(lista):
    """Recibe una lista y un personaje, crea una nueva clave dentro de la lista de diccionarios
    guardando un string en ella y retorna la lista"""
    for personaje in lista:
        codigo_personaje = generar_codigo_personaje(i-1)
        personaje["Codigo"] = codigo_personaje
    
    return lista

menu = ["1: Listar cantidad por raza", "2: Listar personajes por raza"
        ,"3: Listar personajes por habilidad", "4: Jugar batalla" 
        , "5: Encontrar raza y habilidad", "6: Dar poder a los saiyan", "7: Ordenar personajes por atributo "
        ,"8: Generar y agregar codigos de los personajes ", "9: Salir"]

salir = 0
vuelta = 0
while salir == 0:
    for option in menu:
        print(option)
    try:
        option = int(input("Elija la opción a realizar: "))
        match option:
            case 1:
                cantidad_raza("Raza",lista_personajes)
            case 2:
                presonajes_raza(lista_personajes, "Raza", 'Nombre', 'Poder de ataque')
            case 3:
                personajes_habilidad("Habilidades", lista_personajes)
            case 4: 
                jugar_batalla(lista_personajes)
            case 5:
                raza = input("Ingrese una raza: ")
                habilidad = input("Ingrese una Habilidad: ")
                archivo = guardar_json(lista_personajes, raza, habilidad) 
                leer_jason(archivo)
            case 6:
                buffear_saiyan(lista_personajes, "Raza")
            case 7:
                atributo = str(input(f"¿Por que atributo desea ordenar la lista de personajes? \n puede ser por ID, Nombre, Habilidades, Raza, Poder de ataque, Poder de pelea "))
                orden = str(input("¿Desea ordenar los personajes de forma ascendente? responder si/no "))
                if orden == "si":
                    orden = True
                else:
                    orden = False
                print(ordenar_personajes_por_atributo(lista_personajes, atributo, orden))
            case 8:
                i = int(input("¿A que personaje desea generarle un codigo? Por favor escribir el ID de su personaje "))
                print(generar_codigo_personaje(lista_personajes[i-1]))
            case 9:
                salir = 1 
    except:
        print("Ha ocurrido un error, por favor vuelva a intentarlo")
