from random import randrange, shuffle
from typing import List
import random

class Tablero:
    def __init__(self, reinas: List[int]) -> None:
        self.reinas = reinas
        self.fitness_score = self.fitness()

    def calcular_ataques(self):
        ataques = 0
        y_b = 0
        for y_a in range(len(self.reinas)):
            x_a = self.reinas[y_a]

            for y_b in range(y_a + 1, len(self.reinas)):
                x_b = self.reinas[y_b]

                if self.ataques_en_fila(x_a, x_b):
                    ataques += 1
                elif self.ataques_en_diagonal(x_a, y_a, x_b, y_b):
                    ataques += 1

        return ataques

    def ataques_en_fila(self, x_a, x_b):
        return x_a == x_b

    def ataques_en_diagonal(self, x_a, y_a, x_b, y_b):
        return (abs((y_b - y_a) / (x_b - x_a)) == 1 )

    def fitness(self):
        return 28 - self.calcular_ataques()

    def __str__(self) -> str:
        text = "[ "
        for i in self.reinas:
            text += str(i)
            text += ", "
        text += f" fitness = {self.fitness_score}]"
        return text

    @classmethod
    def generar_tablero(cls):
        return Tablero([ randrange(1,9) for _ in range(8)])


class OchoReinasGA:

    def __init__(self) -> None:
        self.TAM_POBLACION = 5
        # La probabilidad de mutacion va de 1 entre 25
        self.PROB_MUTACION = 25

        # Generacion de la poblacion inicial
        self.poblacion = self.generar_poblacion()
        self.poblacion.sort(key=lambda x: x.fitness_score, reverse=True)

        self.solution = None

    def resolver(self):
        i = 0
        while not self.is_solved():

            # Imprimir individuos en la poblacion
            print(f"\n************* ITERACION: {i} *************")
            self.__print_individuos(*self.poblacion)

            # Seleccion de padres
            padre, madre = self.seleccion_padres()

            # Crossover, generacion de hijos
            hijo1, hijo2 = self.crossover(padre, madre)

            # Mutacion de hijos
            self.mutacion(hijo1, hijo2)

            # Modificar la poblacion, para generar la proxima generacion
            self.siguiente_generacion(hijo1, hijo2)


            # Imprimir padres
            print("\n---------------- PADRES ----------------")
            self.__print_individuos(padre, madre)

            # Imprimir hijos
            print("\n---------------- HIJOS -----------------")
            self.__print_individuos(hijo1, hijo2)

            i += 1

    def generar_poblacion(self) -> List[Tablero]:
        # Generamos la poblacion inicial 
        poblacion = [Tablero.generar_tablero() for _ in range(self.TAM_POBLACION)]
        poblacion.sort(key=lambda x: x.fitness_score, reverse=True)
        return poblacion

    def seleccion_padres(self):
        # Calcular la suma total de los valores de fitness en la población
        total_score = sum(indiv.fitness_score for indiv in self.poblacion)

        # Calcular las probabilidades de selección de cada individuo
        probabilities = [indiv.fitness_score / total_score for indiv in self.poblacion]

        # Generar números aleatorios para seleccionar a los padres
        index_padre = self.seleccion_ruleta(probabilities)
        index_madre = self.seleccion_ruleta(probabilities)

        # Asegurarse de que la madre no sea el mismo individuo que el padre
        while index_madre == index_padre:
            index_madre = self.seleccion_ruleta(probabilities)

        padre = self.poblacion[index_padre]
        madre = self.poblacion[index_madre]

        return padre, madre

    def seleccion_ruleta(self, probabilidades):
        ruleta = []

        # Llenar el vector en base a las probabilidades de cada individuo
        for i, prob in enumerate(probabilidades):
            num = int(prob * 100)
            ruleta.extend([i] * num)

        # Seleccionar un índice aleatorio del vector
        selected_index = random.choice(ruleta)

        return selected_index


    def crossover(self, padre: Tablero, madre: Tablero):
        for indiv in self.poblacion:
            size = len(indiv.reinas)
        # print("Longitud ", size)

        # Punto de cruce o corte
        punto = size - 1
        corte = randrange(1, punto)
        # corte = randrange(1,7)
        # print("punto de corte ", corte)
        # Cruce de los genes
        primer_hijo: list[int] = padre.reinas[:corte] + madre.reinas[corte:]
        segundo_hijo: list[int] = madre.reinas[:corte] + padre.reinas[corte:]

        # Generacion de dos hijos con dichos genes
        hijo1 = Tablero(primer_hijo)
        hijo2 = Tablero(segundo_hijo)

        return hijo1, hijo2


    def mutacion(self, hijo1: Tablero, hijo2: Tablero):
            if random.randint(0, 1) == 0:
                if random.randint(0, 100) < self.PROB_MUTACION:
                    hijo1.reinas[random.randint(0, 7)] = random.randint(1, 8)
                    # print("Muto el hijo 1")
            else:
                if random.randint(0, 100) < self.PROB_MUTACION:
                    hijo2.reinas[random.randint(0, 7)] = random.randint(1, 8)
                    # print("Muto el hijo 2")

    def siguiente_generacion(self, hijo1, hijo2):
        self.poblacion.sort(key=lambda x: x.fitness_score)
        del self.poblacion[0]
        del self.poblacion[1]
        self.poblacion.append(hijo1)
        self.poblacion.append(hijo2)

    def is_solved(self):
        for ind in self.poblacion:
            if ind.fitness_score == 28:
                self.solution = ind
                return True
        return False

    def __print_individuos(self, *individuos: Tablero):
        for ind in individuos:
            print(ind)


class Printer:

    def __init__(self) -> None:
        self.tablero_a_imprimir = self.generar_tablero_vacio()

    def generar_tablero_vacio(self):
        # Generacion de una tabla en blanco 
        tablero_a_imprimir = []
        for i in range(9):
            row = []
            if i == 0:
                for j in "12345678":
                    if j == "1":
                        row.append(f"+  {j}")
                    else:
                        row.append(f" {j}")
                tablero_a_imprimir.append(row)
            else: 
                for j in range(9):
                    if j == 0:
                        row.append(f"{i} ")
                    else: 
                        row.append("* ")
                tablero_a_imprimir.append(row)
        return tablero_a_imprimir



    def imprimir_tablero(self, tablero: Tablero):
        self.tablero_a_imprimir = self.generar_tablero_vacio()
        for i in range(8):
            self.tablero_a_imprimir[tablero.reinas[i]][i+1] = "Q "

        print(tablero)
        print("\n")
        for i in range(len(self.tablero_a_imprimir)):
            for j in range(len(self.tablero_a_imprimir[i])):
                print(self.tablero_a_imprimir[i][j], end=" ")
            print("")
        print("\n")



if __name__ == "__main__":
    printer = Printer()

    genetic_algorithm = OchoReinasGA()

    genetic_algorithm.resolver()

    print("\n\n############### SOLUCION ################")
    printer.imprimir_tablero(genetic_algorithm.solution)
