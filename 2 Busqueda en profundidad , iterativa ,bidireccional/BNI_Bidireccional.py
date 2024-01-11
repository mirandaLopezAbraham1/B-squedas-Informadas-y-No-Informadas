from collections import deque
import graphviz


class Arbol:
    def __init__(self):
        self.raiz = None


class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.hijos = []

    def imprimir_dato(self):
        for i in range(4):
            print("|", end="")
            for j in range(3):
                print(f"{self.dato[i][j]}|", end="")
            print("")


class ArbolGeneral:
    def __init__(self):
        # ESTADOS
        # 1.-Mover Derecha
        # 2.-Mover Izquierda
        # 3.-Avanzar Recto
        # Los estados se ejecutan en ese orden
        # Se genera una matriz para saber cómo avanza, donde cada posición estará representada por una letra
        # para conocer cómo avanza. La matriz será de 4x3.
        self.mapa = [
            ["UTA", "A", "B"],
            ["C", "D", "E"],
            ["F", "G", "H"],
            ["I", "J", "MALL"],
        ]

        # El algoritmo será de modo iterativo, se cambiará de posición a UTA hasta llegar a la posición del MALL
        # ejecutando los estados y comprobando cada uno de ellos
        self.arbol_inicial = Arbol()
        self.arbol_final = Arbol()
        # Variables para verificar si se cumple la función objetivo desde ambos extremos
        self.esObjInicial = False
        self.esObjFinal = False
        # Listas de posiciones visitadas para ambos árboles
        self.visitadas_inicial = set()  # Usamos un conjunto para un acceso más rápido
        self.visitadas_final = set()
        # Contadores de nodos en la ruta de camino para ambos árboles
        self.contador_nodos_inicial = 0
        self.contador_nodos_final = 0

    def copia_mapa(self, mapa_origen):
        copia_m = [["" for _ in range(3)] for _ in range(4)]
        for i, fila in enumerate(mapa_origen):
            for j, valor in enumerate(fila):
                copia_m[i][j] = valor
        return copia_m

    def imprimir_arbol(self, arbol):
        if arbol.raiz is None:
            print("El árbol está vacío.")
            return

        # Usamos BFS para recorrer el árbol e imprimir los nodos
        cola = deque()
        cola.append((arbol.raiz, None))

        nivel_actual = 0  # Para rastrear el nivel actual en el árbol
        while cola:
            nodo_actual, padre = cola.popleft()  # Desempaquetamos el nodo y su padre

            # Imprimimos un título cuando empezamos a imprimir los hijos de un nodo
            if nivel_actual != 0:
                print("\n--- Nodo", nivel_actual, "---")

            # Imprimimos el padre y sus hijos
            if padre is not None:
                print("Padre:")
                padre.imprimir_dato()
                print("===============")
            nodo_actual.imprimir_dato()

            # Agregamos los hijos del nodo actual junto con su padre (nodo_actual)
            for hijo in nodo_actual.hijos:
                cola.append((hijo, nodo_actual))

            # Actualizamos el nivel actual cuando llegamos a los hijos
            nivel_actual += 1

        # Imprimir el contador de nodos en la ruta de camino al final
        print("\nCosto del camino:", self.contador_nodos_inicial if arbol == self.arbol_inicial else self.contador_nodos_final)

    def imprimir_ruta(self, solucion):
        ruta = ""
        for i in range(4):
            for j in range(3):
                if solucion[i][j] == "X" or solucion[i][j] == "UTA":
                    ruta += self.mapa[i][j] + "->"
                    if solucion[i][j] == "UTA":
                        self.contador_nodos_inicial += 1
                    else:
                        self.contador_nodos_final += 1
        ruta += "MALL"
        return ruta

    def insertar_hijos(self, nodo, padre, dato):
        # Si la lista de hijos de la raíz es vacía, se insertará ahí
        if nodo.dato == padre:
            # Si se cumple la condición, se crea el hijo
            if len(nodo.hijos) < 3:
                nodo.hijos.append(Nodo(dato))
                return True
        # Si la raíz no es el padre, se procesa a buscar en los hijos
        else:
            # Si el padre es algunos de los hijos
            for hijo in nodo.hijos:
                if hijo.dato == padre:
                    # Se coloca el hijo en el nodo
                    if len(hijo.hijos) < 3:
                        hijo.hijos.append(Nodo(dato))
                        return True
                else:
                    # Busca el padre en otro hijo
                    self.insertar_hijos(hijo, padre, dato)
        return False

    def crear_arbol(self):
        raiz_inicial = self.mapa[3][2]
        raiz_final = self.mapa[0][0]
        self.arbol_inicial.raiz = Nodo(self.mapa)
        self.arbol_final.raiz = Nodo(self.mapa)
        self.visitadas_inicial.add(
            tuple(map(tuple, self.mapa))
        )  # Marcar la posición inicial como visitada en el árbol inicial
        self.visitadas_final.add(
            tuple(map(tuple, self.mapa))
        )  # Marcar la posición inicial como visitada en el árbol final
        self.busquedaBidireccional(self.arbol_inicial, raiz_inicial, self.arbol_final, raiz_final)

    def obtener_posicion_actual(self, mapa_origen):
        for i, fila in enumerate(mapa_origen):
            for j, valor in enumerate(fila):
                if valor == "UTA":
                    return i, j

    def verificar_solucion(self, nodo_inicial, nodo_final):
        # Verificar si ambos árboles han llegado al mismo estado
        for estado_inicial in nodo_inicial.hijos:
            for estado_final in nodo_final.hijos:
                if estado_inicial.dato == estado_final.dato:
                    return True
        return False

    def busquedaBidireccional(self, arbol_inicial, raiz_inicial, arbol_final, raiz_final):
        # Usamos dos colas para realizar la búsqueda bidireccional
        cola_inicial = deque()
        cola_final = deque()
        cola_inicial.append(arbol_inicial.raiz)
        cola_final.append(arbol_final.raiz)

        while not self.esObjInicial and not self.esObjFinal:
            if cola_inicial:
                nodo_actual_inicial = cola_inicial.popleft()
                hoja_inicial = nodo_actual_inicial.dato

                # Realizamos los movimientos y expandimos los nodos en el árbol inicial
                self.mover_derecha(nodo_actual_inicial, cola_inicial, self.visitadas_inicial)
                self.mover_izquierda(nodo_actual_inicial, cola_inicial, self.visitadas_inicial)
                self.avanzar_recto(nodo_actual_inicial, cola_inicial, self.visitadas_inicial)
                self.mover_atras(nodo_actual_inicial, cola_inicial, self.visitadas_inicial)

                if self.verificar_solucion(nodo_actual_inicial, arbol_final.raiz):
                    self.esObjInicial = True
                    break

            if cola_final:
                nodo_actual_final = cola_final.popleft()
                hoja_final = nodo_actual_final.dato

                # Realizamos los movimientos y expandimos los nodos en el árbol final
                self.mover_derecha(nodo_actual_final, cola_final, self.visitadas_final)
                self.mover_izquierda(nodo_actual_final, cola_final, self.visitadas_final)
                self.avanzar_recto(nodo_actual_final, cola_final, self.visitadas_final)
                self.mover_atras(nodo_actual_final, cola_final, self.visitadas_final)

                if self.verificar_solucion(arbol_inicial.raiz, nodo_actual_final):
                    self.esObjFinal = True
                    break

        if self.esObjInicial or self.esObjFinal:
            self.imprimir_arbol(arbol_inicial)
            self.imprimir_arbol(arbol_final)
            print("")

    def mover_derecha(self, nodo, cola, visitadas):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato
        aux = self.copia_mapa(nodo.dato)

        if fila > 0 and aux[fila - 1][columna] not in visitadas:
            FO = padre[fila - 1][columna]
            if FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("********RESPUESTA ENCONTRADA**********")
                    nodo.imprimir_dato()
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))
                    print("")
                    self.esObjInicial = True
                else:
                    aux[fila - 1][columna] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol_inicial.raiz, padre, aux)
                    visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))

    def mover_izquierda(self, nodo, cola, visitadas):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato
        aux = self.copia_mapa(nodo.dato)

        if fila < 3 and aux[fila + 1][columna] not in visitadas:
            FO = padre[fila + 1][columna]
            if FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("********RESPUESTA ENCONTRADA**********")
                    nodo.imprimir_dato()
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))
                    print("")
                    self.esObjInicial = True
                else:
                    aux[fila + 1][columna] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol_inicial.raiz, padre, aux)
                    visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))

    def avanzar_recto(self, nodo, cola, visitadas):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato
        aux = self.copia_mapa(nodo.dato)

        if columna < 2 and aux[fila][columna + 1] not in visitadas:
            FO = padre[fila][columna + 1]
            if FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("********RESPUESTA ENCONTRADA**********")
                    nodo.imprimir_dato()
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))
                    print("")
                    self.esObjInicial = True
                else:
                    aux[fila][columna + 1] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol_inicial.raiz, padre, aux)
                    visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))

    def mover_atras(self, nodo, cola, visitadas):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato
        aux = self.copia_mapa(nodo.dato)

        if columna > 0 and aux[fila][columna - 1] not in visitadas:
            FO = padre[fila][columna - 1]
            if FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("********RESPUESTA ENCONTRADA**********")
                    nodo.imprimir_dato()
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))
                    print("")
                    self.esObjInicial = True
                else:
                    aux[fila][columna - 1] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol_inicial.raiz, padre, aux)
                    visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))

    def imprimir_arbol_con_graphviz(self, arbol, filename="arbol"):
        if arbol.raiz is None:
            print("El árbol está vacío.")
            return

        # Crea un nuevo objeto Graphviz
        dot = graphviz.Digraph(format="png")

        cola = deque()
        cola.append((arbol.raiz, None))

        nivel_actual = 0
        while cola:
            nodo_actual, padre = cola.popleft()

            # Agrega el nodo actual al gráfico
            dot.node(str(nodo_actual), label=str(nodo_actual.dato))

            if padre is not None:
                # Agrega una conexión desde el padre al nodo actual
                dot.edge(str(padre), str(nodo_actual))

            for hijo in nodo_actual.hijos:
                cola.append((hijo, nodo_actual))

        # Genera y guarda el archivo de imagen (formato PNG por defecto)
        dot.render(filename, view=True)


def main():
    ag2 = ArbolGeneral()
    ag2.crear_arbol()
    ag2.imprimir_arbol_con_graphviz(ag2.arbol_inicial, "arbolBidireccional_inicial")
    # ag2.imprimir_arbol_con_graphviz(ag2.arbol_final, "arbolBidireccional_final")

if __name__ == "__main__":
    import time

    start_time = time.time()
    inicio = time.process_time()
    main()
    end_time = time.time()
    fin = time.process_time()

    elapsed_time = end_time - start_time
    total = fin - inicio
    print(f"Tiempo de procesamiento: {total} segundos")
    print(f"Tiempo de ejecucion por epocas: {elapsed_time} segundos")
