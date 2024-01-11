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
        self.PROB_MUTACION = 25
        self.poblacion = self.generar_poblacion()
        self.poblacion.sort(key=lambda x: x.fitness_score, reverse=True)
        self.solution = None

    def resolver(self):
        i = 0
        while True:
            print(f"\n************* ITERACION: {i} *************")
            self.__print_individuos(*self.poblacion)

            padre, madre = self.seleccion_padres()
            hijo1, hijo2 = self.crossover(padre, madre)
            self.mutacion(hijo1, hijo2)

            self.siguiente_generacion(hijo1, hijo2)
            
            self.poblacion.sort(key=lambda x: x.fitness_score, reverse=True)

            print("\n---------------- PADRES ----------------")
            self.__print_individuos(padre, madre)

            print("\n---------------- HIJOS -----------------")

            if self.solution is None or self.poblacion[0].fitness_score > self.solution.fitness_score:
                self.solution = self.poblacion[0]

            i += 1

        if self.is_solved():
            print("¡Se encontró una solución!")
        else:
            print(f"Se alcanzó el límite de iteraciones.")

    def generar_poblacion(self) -> List[Tablero]:
        poblacion = [Tablero.generar_tablero() for _ in range(self.TAM_POBLACION)]
        poblacion.sort(key=lambda x: x.fitness_score, reverse=True)
        return poblacion

    def seleccion_padres(self):
        total_score = sum(indiv.fitness_score for indiv in self.poblacion)
        probabilities = [indiv.fitness_score / total_score for indiv in self.poblacion]
        index_padre = self.seleccion_ruleta(probabilities)
        index_madre = self.seleccion_ruleta(probabilities)
        while index_madre == index_padre:
            index_madre = self.seleccion_ruleta(probabilities)
        padre = self.poblacion[index_padre]
        madre = self.poblacion[index_madre]
        return padre, madre

    def seleccion_ruleta(self, probabilidades):
        ruleta = []
        for i, prob in enumerate(probabilidades):
            num = int(prob * 100)
            ruleta.extend([i] * num)
        selected_index = random.choice(ruleta)
        return selected_index

    def crossover(self, padre: Tablero, madre: Tablero):
        cut = randrange(0, 8)
        primer_hijo = padre.reinas[:cut] + madre.reinas[cut:]
        segundo_hijo = madre.reinas[:cut] + padre.reinas[cut:]
        hijo1 = Tablero(primer_hijo)
        hijo2 = Tablero(segundo_hijo)
        return hijo1, hijo2

    def mutacion(self, hijo1: Tablero, hijo2):
        if random.randint(0, 1) == 0:
            if random.randint(0, 100) < self.PROB_MUTACION:
                hijo1.reinas[random.randint(0, 7)] = random.randint(2, 7)
        else:
            if random.randint(0, 100) < self.PROB_MUTACION:
                hijo2.reinas[random.randint(0, 7)] = random.randint(2, 7)

    def siguiente_generacion(self, hijo1, hijo2):
        poblacion_completa = self.poblacion + [hijo1, hijo2]
        total_score = sum(indiv.fitness_score for indiv in poblacion_completa)
        probabilities = [indiv.fitness_score / total_score for indiv in poblacion_completa]
        ruleta = []
        for i, prob in enumerate(probabilities):
            num = int(prob * 100)
            ruleta.extend([i] * num)
        indexes_to_remove = random.sample(range(len(poblacion_completa)), 2)
        for index in sorted(indexes_to_remove, reverse=True):
            del poblacion_completa[index]
        self.poblacion = poblacion_completa

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
