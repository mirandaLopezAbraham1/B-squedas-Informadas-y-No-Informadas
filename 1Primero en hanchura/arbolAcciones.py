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
        self.arbol = Arbol()  
        # Variable para verificar si se cumple la función objetivo
        self.esObj = False
        # Lista de posiciones visitadas
        self.visitadas = set()  # Usamos un conjunto para un acceso más rápido
        # Contador de nodos en la ruta de camino
        self.contador_nodos = 0

    def copia_mapa(self, mapa_origen):
        copia_m = [["" for _ in range(3)] for _ in range(4)]
        for i, fila in enumerate(mapa_origen):
            for j, valor in enumerate(fila):
                copia_m[i][j] = valor
        return copia_m

    def imprimir_arbol(self):
        if self.arbol.raiz is None:  
            print("El árbol está vacío.")
            return

        # Usamos BFS para recorrer el árbol e imprimir los nodos
        cola = deque()
        cola.append((self.arbol.raiz, None))  

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
        print("\nCosto del camino:", self.contador_nodos)

    def imprimir_ruta(self, solucion):
        ruta = ""
        for i in range(4):
            for j in range(3):
                if solucion[i][j] == "X" or solucion[i][j] == "UTA":
                    ruta += self.mapa[i][j] + "->"
                    self.contador_nodos += 1  # Incrementar el contador de nodos en la ruta de camino
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
        raiz_a = self.mapa[3][2]
        self.arbol.raiz = Nodo(self.mapa)  
        self.visitadas.add(
            tuple(map(tuple, self.mapa))
        )  # Marcar la posición inicial como visitada
        self.busquedaAnchura(self.arbol.raiz)  

    def obtener_posicion_actual(self, mapa_origen):
        for i, fila in enumerate(mapa_origen):
            for j, valor in enumerate(fila):
                if valor == "UTA":
                    return i, j

    def busquedaAnchura(self, nodo):  
        # Usamos una cola en lugar de una lista para implementar BFS
        cola = deque()
        cola.append(nodo)  

        while not self.esObj and cola:
            nodo_actual = cola.popleft()  
            hoja = nodo_actual.dato  

            # Realizamos los movimientos y expandimos los nodos
            self.mover_derecha(nodo_actual, cola)  
            self.mover_izquierda(nodo_actual, cola)  
            self.avanzar_recto(nodo_actual, cola)  
            self.mover_atras(nodo_actual, cola)  

        if self.esObj:
            self.imprimir_arbol()
            print("")

    def mover_derecha(self, nodo, cola):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)  
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato  
        aux = self.copia_mapa(nodo.dato)  

        if fila > 0 and aux[fila - 1][columna] not in self.visitadas:
            FO = padre[fila - 1][columna]
            if  FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("*************************RESPUESTA ENCONTRADA*****************************")
                    nodo.imprimir_dato()  
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))  
                    print("")
                    self.esObj = True
                else:
                    aux[fila - 1][columna] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol.raiz, padre, aux)  
                    self.visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))  

    def mover_izquierda(self, nodo, cola):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)  
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato  
        aux = self.copia_mapa(nodo.dato)  

        if fila < 3 and aux[fila + 1][columna] not in self.visitadas:
            FO = padre[fila + 1][columna]
            if  FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("*************************RESPUESTA ENCONTRADA*****************************")
                    nodo.imprimir_dato()  
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))  
                    print("")
                    self.esObj = True
                else:
                    aux[fila + 1][columna] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol.raiz, padre, aux)  
                    self.visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))  

    def avanzar_recto(self, nodo, cola):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)  
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato  
        aux = self.copia_mapa(nodo.dato)  

        if columna < 2 and aux[fila][columna + 1] not in self.visitadas:
            FO = padre[fila][columna + 1]
            if  FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("*************************RESPUESTA ENCONTRADA*****************************")
                    nodo.imprimir_dato()  
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))  
                    print("")
                    self.esObj = True
                else:
                    aux[fila][columna + 1] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol.raiz, padre, aux)  
                    self.visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))  

    def mover_atras(self, nodo, cola):
        aux_posicion = self.obtener_posicion_actual(nodo.dato)  
        fila = aux_posicion[0]
        columna = aux_posicion[1]
        padre = nodo.dato  
        aux = self.copia_mapa(nodo.dato)  

        if columna > 0 and aux[fila][columna - 1] not in self.visitadas:
            FO = padre[fila][columna - 1]
            if  FO != "X":  # Evitar nodos con "X"
                if FO == "MALL":
                    print("*************************RESPUESTA ENCONTRADA*****************************")
                    nodo.imprimir_dato()  
                    print("")
                    print("------RUTA DEL CAMINO------")
                    print(self.imprimir_ruta(nodo.dato))  
                    print("")
                    self.esObj = True
                else:
                    aux[fila][columna - 1] = "UTA"
                    aux[fila][columna] = "X"
                    self.insertar_hijos(self.arbol.raiz, padre, aux)  
                    self.visitadas.add(tuple(map(tuple, aux)))
                    cola.append(Nodo(aux))  

    def imprimir_arbol_con_graphviz(self, filename="arbol"):
            if self.arbol.raiz is None:
                print("El árbol está vacío.")
                return

            # Crea un nuevo objeto Graphviz
            dot = graphviz.Digraph(format="png")
            
            cola = deque()
            cola.append((self.arbol.raiz, None))

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
    ag2.imprimir_arbol_con_graphviz("arbol")  # Llama a la función para imprimir el árbol

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
