import random

def generar_solucion_aleatoria(n):
    solucion = list(range(n))
    random.shuffle(solucion)
    return solucion

def generar_vecino_aleatorio(solucion):
    n = len(solucion)
    vecino = list(solucion)
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    vecino[i] = j
    return vecino

def funcion_objetivo(solucion):
    n = len(solucion)
    ataques = 0

    for i in range(n):
        for j in range(i + 1, n):
            if solucion[i] == solucion[j] or abs(solucion[i] - solucion[j]) == j - i:
                ataques += 1

    return -ataques  # Minimizar el número de ataques

def imprimir_tablero(solucion):
    n = len(solucion)
    for i in range(n):
        row = ['Q' if solucion[j] == i else '.' for j in range(n)]
        print(' '.join(row))
    print()

def ascenso_colinas_estocastico(problema):
    solucion_actual = generar_solucion_aleatoria(len(problema))
    mejor_solucion = solucion_actual[:]
    iteraciones = 0

    print("Estado Inicial:")
    imprimir_tablero(solucion_actual)

    while True:
        iteraciones += 1

        vecino = generar_vecino_aleatorio(solucion_actual)
        if funcion_objetivo(vecino) >= funcion_objetivo(solucion_actual) or random.random() < 0.1:
            solucion_actual = vecino

        if funcion_objetivo(solucion_actual) > funcion_objetivo(mejor_solucion):
            mejor_solucion = solucion_actual[:]

        num_ataques = funcion_objetivo(mejor_solucion)
        print(f"Iteración {iteraciones} - Número de ataques: {num_ataques}")
        imprimir_tablero(solucion_actual)

        if num_ataques == 0:
            print("¡Solución óptima encontrada!")
            imprimir_tablero(mejor_solucion)
            break

# Ejemplo de uso para el problema de las 8 reinas
n = 8
ascenso_colinas_estocastico(range(n))