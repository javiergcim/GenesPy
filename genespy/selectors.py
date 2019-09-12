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

from math import floor
from random import random, sample


def select_vasconcelos(task, args):
    """ Realiza cruzas con el método Vasconcelos, con probabilidad *cp*. Los
    cambios en la población son realizados in-situ en el objeto Task pasado como
    referencia. Los hijos sustituyen a los padres.

    Se asume que hay definida una función de cruza que regresa dos
    descendientes.

    Args:
        task (Task): Una referencia la tarea invoulcrada.
        args (dict): Un arreglo con los argumentos propios de la función. *cp*
            indica la propabilidad de cruzamiento.

    """

    cp = args['cp']
    mayor = task.get_size() - 1
    max_minor = floor(mayor / 2.0) + 1
    population = task.get_population()

    # Hacemos la selección (mejor contra peor)
    for minor in range(max_minor):
        # Si el dado favorece, se hace la cruza
        p = random()
        if p < cp:
            childs = task.apply_crossover(population[minor],
                                          population[mayor])
            population[minor] = childs[0]
            population[mayor] = childs[1]
        mayor -= 1


def select_tournament(task, args):
    """ Realiza cruzas utilizando el método de selección por torneo, eligiendo
    dos padres para cada cruza, y anexando al final los descendientes
    resultantes a la población actual de la tarea.

    Se asume que hay definida una función de cruza que regresa dos
    descendientes.

    Args:
        task (Task): Una referencia la tarea invoulcrada.
        args (dict): Un arreglo con los argumentos propios de la función. *k*
            indica el número de individuos en el torneo. El argumento *matchs*
            indica cuantos torneos se llevarán a cabo.

    """

    k = args['k']
    if 'obj_index' in args:
        obj_index = args['obj_index']
    else:
        obj_index = 0
    population = task.get_population()
    p_type = task.get_obj_factors(obj_index)
    matchs = args['matchs']
    childs = {}

    for pair in range(matchs):
        # Elegimos padres
        parents_index = []
        for _ in range(2):
            # Hago el torneo
            tournament = sample(range(len(population)), k)
            best = None
            best_i = None
            for i in tournament:
                current_fitness = population[i].get_fitness(obj_index)
                # Verificamos si es maximización o minimización
                if p_type > 0.0:
                    if best is None or current_fitness > best:
                        best = current_fitness
                        best_i = i
                else:
                    if best is None or current_fitness < best:
                        best = current_fitness
                        best_i = i

            parents_index.append(best_i)

        son_a, son_b = task.apply_crossover(population[parents_index[0]],
                                            population[parents_index[1]])

        childs[parents_index[0]] = son_a
        childs[parents_index[1]] = son_b

    # Se integra toda la descendencia en la población (sustituyen a padres)
    for index, new_born in childs.items():
        population[index] = new_born
