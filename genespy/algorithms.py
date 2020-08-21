# This file is part of GenesPy.
#
# GenesPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# GenesPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with GenesPy. If not, see <http://www.gnu.org/licenses/>.

from time import time
from math import floor, pi, cos


def general_ga(task,
               elitism,
               sec,
               gen=float('inf'),
               verbose=float('inf'),
               report=None):
    """ Ejecuta una algoritmo genético genérico, con posibilidad de elitismo.

    Args:
        task (Task): Un objeto *Task* con los parámetros y la población
            requerida para la ejecución del algoritmo.
        elitism (float): Porcentaje de individuos que se guardarán como elite
            para la siguiente generación.
        sec (float): Segundos que aproximadamente correrá el algoritmo.
        gen (int): Generaciones que se ejecutara el algoritmo genético.
        verbose (int): Indica cada cuantas generaciones se reportan avances.
        report (function|None): Función de reporte. Recibirá la generación y
            mejor fitness de la iteración actual, cada tantas generaciones como
            se especifique según *verbose*.

    Returns:
        Individual: El individuo con mejor aptitud al momento de finalizar la
            corrida.

    """

    inf = float('inf')

    # Se inicia la toma de tiempo
    start_time = time()

    # Se precalcula el número de individuos elite
    n_elite = floor(task.get_size() * elitism)

    task.evaluate()
    task.order_population()

    for g in range(gen):
        task.set_generation(g)

        elite_pop = task.get_subpopulation_copy(slice(n_elite))
        task.apply_selection()
        task.mutate()
        task.evaluate()
        task.append_population(elite_pop, True)
        task.remove_duplicate_fitness()
        if task.adjust_population_size():
            task.evaluate()
            task.order_population()

        # Se verifica si se debe imprimir
        if verbose != inf:
            if g % verbose == 0:
                if report is not None:
                    report(
                        g,
                        task.get_individual(0).get_fitness(),
                        task.get_individual(0).get_genome()
                    )
                else:
                    print('Generation:', g)
                    print(
                        'Best fitness:',
                        task.get_individual(0).get_fitness(),
                        '\n'
                    )

        # Verificamos si se ha cumplido el tiempo
        current_time = time() - start_time
        if current_time > sec:
            break

    task.set_generation(None)

    # Se regresa la solución (el mejor es el primer elemento)
    return task.get_individual(0)


def cos_mutation_ga(task,
                    max_mp,
                    cycle_mp,
                    elitism,
                    sec,
                    gen=float('inf'),
                    verbose=float('inf'),
                    report=None):
    """ Ejecuta una algoritmo genético genérico, con posibilidad de elitismo,
    que genera una probabilidad de mutación *mp* variable a lo largo de las
    generaciones, de acuerdo a una función coseno.

    Args:
        task (Task): Un objeto *Task* con los parámetros y la población
            requerida para la ejecución del algoritmo.
        max_mp (float): Probabilidad máxima de mutación.
        cycle_mp (float): Indica cuantas generaciones dura un ciclo en el
            cambio de valor de la propabilidad de mutación.
        elitism (float): Porcentaje de individuos que se guardarán como elite
            para la siguiente generación.
        sec (float): Segundos que aproximadamente correrá el algoritmo.
        gen (int): Generaciones que se ejecutará el algoritmo genético.
        verbose (int): Indica cada cuantas generaciones se reportan avances.
        report (function|None): Función de reporte. Recibirá la generación y
            mejor fitness de la iteración actual, cada tantas generaciones como
            se especifique según *verbose*.

    Returns:
        Individual: El individuo con mejor aptitud al momento de finalizar la
            corrida.

    """

    inf = float('inf')

    # Se inicia la toma de tiempo
    start_time = time()

    # Ajustamos factores alusivos a mp variable
    cycle_mp = (2.0 * pi) / cycle_mp
    half_max_mp = max_mp / 2.0

    # Calculamos la probabilidad de mutación para ésta generación
    task.set_mutator_arg('mp', max_mp)

    # Se precalcula el número de individuos elite
    n_elite = floor(task.get_size() * elitism)

    task.evaluate()
    task.order_population()

    for g in range(gen):
        task.set_generation(g)

        # Calculamos la probabilidad de mutación para ésta generación
        task.set_mutator_arg(
                'mp',
                (cos(g * cycle_mp) * half_max_mp) + half_max_mp)

        elite_pop = task.get_subpopulation_copy(slice(n_elite))
        task.apply_selection()
        task.mutate()
        task.evaluate()
        task.append_population(elite_pop, True)
        task.remove_duplicate_fitness()
        if task.adjust_population_size():
            task.evaluate()
            task.order_population()

        # Se verifica si se debe imprimir
        if verbose != inf:
            if g % verbose == 0:
                if report is not None:
                    report(
                        g,
                        task.get_individual(0).get_fitness(),
                        task.get_individual(0).get_genome()
                    )
                else:
                    print('Generation:', g)
                    print(
                        'Best fitness:',
                        task.get_individual(0).get_fitness(),
                        '\n'
                    )

        # Verificamos si se ha cumplido el tiempo
        current_time = time() - start_time
        if current_time > sec:
            break

    task.set_generation(None)

    # Se regresa la solución (el mejor es el primer elemento)
    return task.get_individual(0)
