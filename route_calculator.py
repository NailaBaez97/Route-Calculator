def imprimir_mapa(mapa):
    for fila in mapa:
        print(" ".join(str(cell) for cell in fila))

def datos_usuario():
    while True:
        filas = int(input("Ingrese la cantidad de filas: "))
        columnas = int(input("Ingrese la cantidad de columnas: "))
        if filas < 3 or columnas < 3:
            print("El tamaño ingresado no es válido")
        elif filas >= 3 and columnas >= 3:
            break

    mapa = [["."] * columnas for _ in range(filas)]

    inicio = input("Ingrese las coordenadas de Inicio (x,y) separadas por comas: ")
    x_inicio, y_inicio = map(int, inicio.split(','))

    fin = input("Ingrese las coordenadas de fin (x,y) separadas por comas: ")
    x_fin, y_fin = map(int, fin.split(','))

    # Validación de coordenadas dentro del rango
    if x_inicio < 0 or x_inicio >= columnas or y_inicio < 0 or y_inicio >= filas:
        print("La coordenada de inicio está fuera de rango")
        return None

    if x_fin < 0 or x_fin >= columnas or y_fin < 0 or y_fin >= filas:
        print("La coordenada de fin está fuera de rango")
        return None

    # Si se llega aquí, las coordenadas están dentro del rango válido
    mapa[y_inicio][x_inicio] = "I"
    mapa[y_fin][x_fin] = "F"

    imprimir_mapa(mapa)

    obstaculos = int(input("Ingrese la cantidad de obstáculos que desee: "))

    for i in range(obstaculos):
        while True:
            posicion_obstaculos = input(f"Ingrese la coordenada del obstáculo nro {i+1} (x,y) separadas por comas: ")
            x_obstaculo, y_obstaculo = map(int, posicion_obstaculos.split(','))

            if x_obstaculo < 0 or x_obstaculo >= columnas or y_obstaculo < 0 or y_obstaculo >= filas:
                print("Las coordenadas del obstáculo están fuera del rango.")
            elif (x_obstaculo == x_inicio and y_obstaculo == y_inicio) or (x_obstaculo == x_fin and y_obstaculo == y_fin):
                print("La coordenada no puede estar en la posición del inicio o fin.")
            else:
                mapa[y_obstaculo][x_obstaculo] = "X"
                break

    imprimir_mapa(mapa)
    return mapa, x_inicio, y_inicio, x_fin, y_fin  # Retorno de valores actualizado

def heuristica(nodo, fin):
    # Distancia Manhattan
    return abs(nodo[0] - fin[0]) + abs(nodo[1] - fin[1])

def obtener_vecinos(nodo, mapa):
    vecinos = []
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for movimiento in movimientos:
        nueva_posicion = nodo[0] + movimiento[0], nodo[1] + movimiento[1]

        if 0 <= nueva_posicion[0] < len(mapa[0]) and 0 <= nueva_posicion[1] < len(mapa): #esta dentro del mapa
            if mapa[nueva_posicion[1]][nueva_posicion[0]] != "X": #y no es un obstaculo
                vecinos.append(nueva_posicion)

    return vecinos
        
def construir_camino(padres, nodo_final, mapa):
    camino = []
    actual = nodo_final

    while actual:
        camino.append(actual)
        actual = padres.get(actual)
    camino.reverse()

    # Diccionario para marcar el camino en el mapa
    camino_diccionario = {}

    for (x, y) in camino:
        if mapa[y][x] not in ("I", "F"):
            camino_diccionario[(x, y)] = '*'

    return camino_diccionario

def implementacion_algoritmo(x_inicio, y_inicio, x_fin, y_fin, mapa):
    lista_visitar = []  # Los nodos a ser evaluados 
    lista_visitado = []  # Los nodos evaluados
    nodo_inicial = (x_inicio, y_inicio)  # Nodo inicial
    nodo_final = (x_fin, y_fin)  # Nodo final

    lista_visitar.append(nodo_inicial)

    # Inicialización de g, h, f para el nodo inicial(diccionarios)
    g = {nodo_inicial: 0}
    h = {nodo_inicial: heuristica(nodo_inicial, nodo_final)}
    f = {nodo_inicial: h[nodo_inicial]}
    padres = {nodo_inicial: None}

    while lista_visitar:
        menor_costo = min(lista_visitar, key=lambda nodo: f[nodo])

        if menor_costo == nodo_final:
            camino_diccionario = construir_camino(padres, nodo_final, mapa)  # Obtener diccionario de coordenadas
            for (x, y), valor in camino_diccionario.items():
                mapa[y][x] = valor  # Marcar el camino en el mapa
            return camino_diccionario  # Puedes devolver el diccionario si lo necesitas

        lista_visitar.remove(menor_costo)
        lista_visitado.append(menor_costo)

        for vecino in obtener_vecinos(menor_costo, mapa):
            if vecino in lista_visitado:
                continue

            tentative_g = g[menor_costo] + 1

            if vecino not in lista_visitar:
                lista_visitar.append(vecino)
            elif tentative_g >= g.get(vecino, float('inf')):
                continue

            padres[vecino] = menor_costo#registra menor costo como el padre vecino
            g[vecino] = tentative_g #actualiza
            h[vecino] = heuristica(vecino, nodo_final)
            f[vecino] = g[vecino] + h[vecino]

    return None


mapa, x_inicio, y_inicio, x_fin, y_fin = datos_usuario()

if mapa:
    camino_diccionario = implementacion_algoritmo(x_inicio, y_inicio, x_fin, y_fin, mapa)

    if camino_diccionario:
        # Imprimir mapa con el camino marcado
        imprimir_mapa(mapa)
    else:
        print("No se encontró un camino válido.")
#calculadora-de-rutas
