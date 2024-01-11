from random import shuffle
from typing import List
from enum import Enum
import graphviz

class Movimientos(Enum):
    DERECHA = "DERECHA"
    IZQUIERDA = "IZQUIERDA"
    ARRIBA = "ARRIBA"
    ABAJO = "ABAJO"

class Puzzle:
    def __init__(self, matrix: List[List[int]], obj: List[List[int]]) -> None:
        self.matrix = matrix
        self.obj = obj
        self.definir_posicion_zero()

    def random_puzzle():
        casilla = []
        numeros = list(range(0, 9))
        shuffle(numeros)
        for row in range(3):
            casilla.append([])
            for col in range(3):
                casilla[row].append(numeros.pop())
        return casilla

    def obtener_posicion(self, number, where):
        for i in range(len(where)):
            for j in range(len(where)):
                if where[i][j] == number:
                    return [i,j]
        return [-1,-1]

    def heuristica(self):
        total = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != self.obj[i][j]:
                    total += 1
        return total

    def definir_posicion_zero(self) -> None: 
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    self.i = i
                    self.j = j
    def mover(self, direccion: Movimientos) -> bool: 
        movimientos = {
            Movimientos.ARRIBA: self.mover_arriba,
            Movimientos.ABAJO: self.mover_abajo,
            Movimientos.DERECHA: self.mover_derecha,
            Movimientos.IZQUIERDA: self.mover_izquierda,
        }
        if self.check_movimiento(direccion):
            movimientos[direccion]() 
            self.definir_posicion_zero()
            return True
        else:
            return False

    def check_movimiento(self, direccion: Movimientos) -> bool: 
        direcciones = { 
            Movimientos.ARRIBA: self.i != 0,
            Movimientos.ABAJO: self.i != 2,
            Movimientos.DERECHA: self.j != 2,
            Movimientos.IZQUIERDA: self.j != 0
        }
        return direcciones[direccion]

    def esta_resuelto(self) -> bool:
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != self.obj[i][j]:
                    return False
        return True

    def equals(self, puzzle) -> bool:
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != puzzle.matrix[i][j]:
                    return False
        return True


    def print(self, spaces = ''): 
        color = '\033[93m'
        end = '\033[0m'
        text = ""
        esta_resuelto = self.esta_resuelto()
        if esta_resuelto:
         text = color
        text += spaces + "_____ \n"
        blanks = ""
        for i in range(len(spaces)):
            if i == len(spaces)-3:
                blanks += "|"
            else:
                blanks += " "
        for row in self.matrix:
            text += blanks
            for n in row:
                text +=  str(n) + ' '
            text += '\n'
        text += spaces + '_____ '
        if esta_resuelto: 
            text += end
        return text

    
    def get_matrix(self) -> List[List[int]]:
        new_matrix = []
        for row in self.matrix:
            new_row = []
            for j in row:
                new_row.append(j)
            new_matrix.append(new_row)
        return new_matrix

    def conteo_de_inversas(self, arr):
        inv_count = 0
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
        return inv_count
 
    def es_solucionable(self):
        inv_count = self.conteo_de_inversas([j for sub in self.matrix for j in sub])
        return (inv_count % 2 == 0)

    def mover_arriba(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i-1][self.j]
        self.matrix[self.i-1][self.j] = 0

    def mover_abajo(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i+1][self.j]
        self.matrix[self.i+1][self.j] = 0

    def mover_derecha(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i][self.j+1]
        self.matrix[self.i][self.j+1] = 0

    def mover_izquierda(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i][self.j-1]
        self.matrix[self.i][self.j-1] = 0

    def mas_de_un_cero(self):
        count = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    count += 1
        return count > 1
    
    def __str__(self):
        result = ""
        for row in self.matrix:
            result += " ".join(map(str, row)) + "\n"
        return result


class Nodo:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.parent = None
        self.children = []

    def add_hijo(self, puzzle):
        if self.es_repetido(puzzle):
            return
        child = Nodo(puzzle)
        child.parent = self
        self.children.append(child)

    def es_repetido(self, puzzle):
        if self.parent:
            return self.parent.puzzle.equals(puzzle)

    def generar_hijos(self):
        if self.puzzle.esta_resuelto():
            return self
        for i in Movimientos:
            matrix = self.puzzle.get_matrix()
            new_puzzle = Puzzle(matrix, self.puzzle.obj)
            if new_puzzle.mover(i):
                self.add_hijo(new_puzzle)
        return None

    def es_hoja(self):
        if len(self.children) > 0:
            return False
        return True

    def funcion_costo(self):
        return self.costo_camino_acumulado() + self.puzzle.heuristica()

    def costo_camino_acumulado(self):
        nivel = 0
        p = self.parent
        while p:
            nivel += 1
            p = p.parent
        return nivel

    def buscar_nodoHoja_menor_o_igual(self, lowest):
        if self.es_hoja() and self.f_menor_o_igual(lowest):
            return self
        if self.children:
            for child in self.children:
                lowest = child.buscar_nodoHoja_menor_o_igual(lowest)
        return lowest

    def buscar_nodoHoja_menor(self, lowest):
        if self.es_hoja() and self.f_menor_que(lowest):
            return self
        if self.children:
            for child in self.children:
                lowest = child.buscar_nodoHoja_menor(lowest)
        return lowest

    def existe_nodoHoja_menor(self, node) -> bool:
        if self.es_hoja() and self.f_menor_que(node):
            return True 
        exists = False
        if self.children:
            for child in self.children:
                 exists = child.existe_nodoHoja_menor(node)
                 if exists:
                    break
        return exists

    def buscar_primer_nodoHoja(self):
        if self.es_hoja():
            return self
        if self.children:
            for child in self.children:
                return child.buscar_primer_nodoHoja()

    def f_menor_o_igual(self, other) -> bool:
        return self.funcion_costo() <= other.funcion_costo()

    def f_menor_que(self, other) -> bool:
        return self.funcion_costo() < other.funcion_costo()

class Arbol:
    def __init__(self, puzzle: Puzzle) -> None:
        self.raiz = None
        self.puzzle = puzzle
        self.solution = None
        self.leafs = []
        self.nodos_abiertos = 0
        self.iteracion = 0


    def resolver(self) -> None:
        self.raiz = Nodo(self.puzzle)
        self.current = self.raiz
        self.leafs.append(self.raiz)
        while (self.solution is None 
            or self.solution is not self.raiz.buscar_nodoHoja_menor_o_igual(self.solution)):
            self.iteracion += 1
            print(f"Iteracion: {self.iteracion}")

            leaf_node = self.leafs[0]
            self.current = self.raiz.buscar_nodoHoja_menor_o_igual(leaf_node)

            if self.current:
                self.solution = self.current.generar_hijos()
                if self.current.children:
                    self.leafs.remove(self.current)
                    self.nodos_abiertos += 1
                    for child in self.current.children:
                        self.leafs.append(child)

            self.leafs.sort(key=lambda hoja: hoja.funcion_costo())

class Printer:
    def __init__(self, tree: Arbol) -> None:
        self.tree = tree
        self.raiz = tree.raiz
        self.color = '\033[93m'
        self.end = '\033[0m'
        self.dot = graphviz.Digraph(comment='ArbolDeBusqueda', format='png')
        self.crear_grafo(self.tree.raiz)

    def imprimir_arbol(self):
        if self.raiz:
            self.imprimir_nodo(self.raiz)
        else:
            print("Sin Raiz")

    def imprimir_info_arbol(self):
        print(f"Numero de hojas: {len(self.tree.leafs)}")
        print(f"Numero de nodos abiertos: {self.tree.nodos_abiertos}")

    def imprimir_info_arbol_formateada(self, node, prefix):
        esta_resuelto = node.puzzle.esta_resuelto()
        text = ""
        if esta_resuelto:
            text += self.color
        text += f"{prefix} g(n) = {node.costo_camino_acumulado()}, h(n) = {node.puzzle.heuristica()}, f(n) = {node.funcion_costo()}, hoja={' SI' if node.es_hoja() else ' NO'} "
        if esta_resuelto:
            text += f"{'****SOLUCION*****' if esta_resuelto else ''}{self.end}"
        print(text)

    def imprimir_nodo(self, node):
        spaces = " " * node.costo_camino_acumulado() * 5
        prefix = spaces + "|__" if node.parent else ""
        self.imprimir_info_arbol_formateada(node, prefix)
        print(node.puzzle.print(prefix))
        if node.children:
            for child in node.children:
                self.imprimir_nodo(child)

    def print_as_child(self, node):
        spaces = "  "
        prefix = spaces + "|__" if node.parent else ""
        self.imprimir_info_arbol_formateada(node, prefix)
        print(node.puzzle.print(prefix))
        if node.children:
            for child in node.children:
                self.imprimir_nodo(child)

    def print_pasos_solution(self):
        current = self.tree.solution
        pasos = []
        while current: 
            pasos.append(current.puzzle)
            current = current.parent
        pasos.reverse()
        i = 0
        for puzzle in pasos:
            print(f"Paso: {i}")
            print(puzzle.print())
            i += 1
    
    def crear_grafo(self, node):
        label = f"{node.puzzle}\n"
        label += f"G(n): {node.costo_camino_acumulado()}\n"
        label += f"H(n): {node.puzzle.heuristica()}\n"
        label += f"F(n): {node.funcion_costo()}\n"
        label += f"Es hoja: {'SI' if node.es_hoja() else 'NO'}"

        self.dot.node(str(node.puzzle), label=label)

        if node.parent:
            self.dot.edge(str(node.parent.puzzle), str(node.puzzle))

        if node.children:
            for child in node.children:
                self.crear_grafo(child)

    def render_tree(self):
        self.dot.render('Arbol_Busqueda_Estrella', view=True)


# -------------------------------------
def main():
    inicio = Puzzle.random_puzzle()
    """
    inicio = [[4, 6, 1], 
                 [0, 5, 3], 
                 [2, 7, 8]]
    """

    objetivo = [[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 0]]

    puzzle = Puzzle(inicio, objetivo)
    
    tree = Arbol(puzzle)
    tree.resolver()

    printer = Printer(tree)

    print("Arbol")
    print(printer.imprimir_arbol())
    print("Pasos de la solucion")
    print(printer.print_pasos_solution())
    print(printer.imprimir_info_arbol())

    printer.render_tree()

if __name__ == "__main__":
    main()