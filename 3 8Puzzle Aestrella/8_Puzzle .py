from random import shuffle
from typing import List
from enum import Enum

class Utils:
    def random_puzzle():
        cells = []
        numbers = list(range(0, 9))
        shuffle(numbers)
        for row in range(3):
            cells.append([])
            for col in range(3):
                cells[row].append(numbers.pop())
        return cells

    def print_selection(puzzle):
        print("Puzzle seleccionado")
        print("Estado Inicial")
        print(puzzle.print())
        print("Estado Objetivo")
        print(puzzle.print_objective())

class Moves(Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    UP = "UP"
    DOWN = "DOWN"

class Puzzle:
    def __init__(self, matrix: List[List[int]], obj: List[List[int]]) -> None:
        self.matrix = matrix
        self.obj = obj
        self.__set_zero_position()

    def __get_position(self, number, where):
        for i in range(len(where)):
            for j in range(len(where)):
                if where[i][j] == number:
                    return [i,j]
        return [-1,-1]

    def h(self):
        total = 0
        for i in range(1,9):
            i_o, j_o = self.__get_position(i, self.matrix)
            i_f, j_f = self.__get_position(i, self.obj)
            i_h = abs(i_o-i_f)
            j_h = abs(j_o-j_f)
            total += i_h + j_h
        return total

    def __set_zero_position(self) -> None: 
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    self.i = i
                    self.j = j
    def move(self, direction: Moves) -> bool: 
        moves = {
            Moves.UP: self.__move_up,
            Moves.DOWN: self.__move_down,
            Moves.RIGHT: self.__move_right,
            Moves.LEFT: self.__move_left,
        }
        if self.check_move(direction):
            moves[direction]() 
            self.__set_zero_position()
            return True
        else:
            #print(f"Cannot move that direction: {direction} i: {self.i} j: {self.j}")
            return False

    def check_move(self, direction: Moves) -> bool: 
        directions = { 
            Moves.UP: self.i != 0,
            Moves.DOWN: self.i != 2,
            Moves.RIGHT: self.j != 2,
            Moves.LEFT: self.j != 0
        }
        return directions[direction]

    def is_solved(self) -> bool:
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
        is_solved = self.is_solved()
        if is_solved:
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
        if is_solved: 
            text += end
        return text

    def print_objective(self, spaces = ''):
        text = spaces + "_____ \n"
        blanks = ""
        for i in range(len(spaces)):
            if i == len(spaces)-3:
                blanks += "|"
            else:
                blanks += " "
        for row in self.obj:
            text += blanks
            for n in row:
                text +=  str(n) + ' '
            text += '\n'
        text += spaces + '_____ '
        return text

    
    def get_matrix(self) -> List[List[int]]:
        new_matrix = []
        for row in self.matrix:
            new_row = []
            for j in row:
                new_row.append(j)
            new_matrix.append(new_row)
        return new_matrix

    def get_inv_count(self, arr):
        inv_count = 0
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
        return inv_count
 
    def is_solvable(self):
        inv_count = self.get_inv_count([j for sub in self.matrix for j in sub])
        return (inv_count % 2 == 0)

    def __move_up(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i-1][self.j]
        self.matrix[self.i-1][self.j] = 0

    def __move_down(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i+1][self.j]
        self.matrix[self.i+1][self.j] = 0

    def __move_right(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i][self.j+1]
        self.matrix[self.i][self.j+1] = 0

    def __move_left(self) -> None: 
        self.matrix[self.i][self.j] = self.matrix[self.i][self.j-1]
        self.matrix[self.i][self.j-1] = 0

    def has_more_than_one_zero(self):
        count = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    count += 1
        return count > 1


class Node:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.parent = None
        self.children = []

    def add_child(self, puzzle):
        if self.is_repeated(puzzle):
            return
        child = Node(puzzle)
        child.parent = self
        self.children.append(child)

    def is_repeated(self, puzzle):
        if self.parent:
            return self.parent.puzzle.equals(puzzle)

    def generate_children(self):
        if self.puzzle.is_solved():
            return self
        for i in Moves:
            matrix = self.puzzle.get_matrix()
            new_puzzle = Puzzle(matrix, self.puzzle.obj)
            if new_puzzle.move(i):
                self.add_child(new_puzzle)
        return None

    def is_leaf(self):
        if len(self.children) > 0:
            return False
        return True

    def f(self):
        return self.g() + self.puzzle.h()

    def g(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def search_leaf_node_lower_or_equal_than(self, lowest):
        if self.is_leaf() and self.lower_or_equal_f_than(lowest):
            return self
        if self.children:
            for child in self.children:
                lowest = child.search_leaf_node_lower_or_equal_than(lowest)
        return lowest

    def search_leaf_node_lower_than(self, lowest):
        if self.is_leaf() and self.lower_f_than(lowest):
            return self
        if self.children:
            for child in self.children:
                lowest = child.search_leaf_node_lower_than(lowest)
        return lowest

    def exists_leaf_node_lower_than(self, node) -> bool:
        if self.is_leaf() and self.lower_f_than(node):
            return True 
        exists = False
        if self.children:
            for child in self.children:
                 exists = child.exists_leaf_node_lower_than(node)
                 if exists:
                    break
        return exists

    def search_first_leaf_node(self):
        if self.is_leaf():
            return self
        if self.children:
            for child in self.children:
                return child.search_first_leaf_node()

    def lower_or_equal_f_than(self, other) -> bool:
        return self.f() <= other.f()

    def lower_f_than(self, other) -> bool:
        return self.f() < other.f()

class Tree:
    def __init__(self, puzzle: Puzzle) -> None:
        self.root = None
        self.puzzle = puzzle
        self.solution = None
        self.leafs = []
        self.open_nodes = 0
        self.iter = 0


    def solve(self) -> None:
        self.root = Node(self.puzzle)
        self.current = self.root
        self.leafs.append(self.root)
        while (self.solution is None 
            or self.solution is not self.root.search_leaf_node_lower_or_equal_than(self.solution)):
            self.iter += 1
            print(f"Busqueda: {self.iter}")

            leaf_node = self.leafs[0]
            self.current = self.root.search_leaf_node_lower_or_equal_than(leaf_node)

            if self.current:
                self.solution = self.current.generate_children()
                if self.current.children:
                    self.leafs.remove(self.current)
                    self.open_nodes += 1
                    for child in self.current.children:
                        self.leafs.append(child)

            self.leafs.sort(key=lambda hoja: hoja.f())

class TreePrinter:
    def __init__(self, tree: Tree) -> None:
        self.tree = tree
        self.root = tree.root
        self.color = '\033[93m'
        self.end = '\033[0m'

    def print_tree(self):
        if self.root:
            self.print_node(self.root)
        else:
            print("None root")

    def print_tree_info(self):
        print(f"Numero de hojas: {len(self.tree.leafs)}")
        print(f"Numero de nodos abiertos: {self.tree.open_nodes}")

    def print_formatted_node_info(self, node, prefix):
        is_solved = node.puzzle.is_solved()
        text = ""
        if is_solved:
            text += self.color
        text += f"{prefix} g(n) = {node.g()}, h(n) = {node.puzzle.h()}, f(n) = {node.f()}, hoja={' SI' if node.is_leaf() else ' NO'} "
        if is_solved:
            text += f"{'****SOLUCION*****' if is_solved else ''}{self.end}"
        print(text)

    def print_node(self, node):
        spaces = " " * node.g() * 5
        prefix = spaces + "|__" if node.parent else ""
        self.print_formatted_node_info(node, prefix)
        print(node.puzzle.print(prefix))
        if node.children:
            for child in node.children:
                self.print_node(child)

    def print_as_child(self, node):
        spaces = "  "
        prefix = spaces + "|__" if node.parent else ""
        self.print_formatted_node_info(node, prefix)
        print(node.puzzle.print(prefix))
        if node.children:
            for child in node.children:
                self.print_node(child)

    def print_alone(self, node):
        print(f"f = {node.f()}")
        print(node.puzzle.print())

    def print_with_children(self, node):
        print(node.puzzle.print())
        self.print_formatted_node_info(node, '')
        if node.children:
            for child in node.children:
                self.print_as_child(child)

    def print_steps_solution(self):
        current = self.tree.solution
        steps = []
        while current: 
            steps.append(current.puzzle)
            current = current.parent
        steps.reverse()
        i = 0
        for puzzle in steps:
            print(f"Paso: {i}")
            print(puzzle.print())
            i += 1

# -------------------------------------
def main():
    init = Utils.random_puzzle()

    objective = [[1, 2, 3], 
                 [4, 5, 6], 
                 [7, 8, 0]]

    puzzle = Puzzle(init, objective)

    while not puzzle.is_solvable():
        puzzle.matrix = Utils.random_puzzle()
    

    tree = Tree(puzzle)
    tree.solve()

    printer = TreePrinter(tree)


    # menu(printer)
    print(printer.print_tree())
    print("Pasos de la solucion")
    print(printer.print_steps_solution())


if __name__ == "__main__":
    main()