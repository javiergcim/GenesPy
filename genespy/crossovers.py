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

from random import randrange, sample
from copy import copy
from itertools import cycle
from .individual import Individual


def crossover_scx(task, ind_a, ind_b, args):
    """ Hace un cruzamiento de genomas que codifican una permutación de destinos
    para el problema del agente viajero, inspirado en SCX.

    El algoritmo genera dos hijos. Uno calculado de derecha a izquierda y otro
    de izquierda a derecha.

    Se asume que el primer objetivo de la tarea asociada determina si el
    problema se maximiza o minimiza.

    Ahmed, Z. H. (2010). Genetic algorithm for the traveling salesman problem
    using sequential constructive crossover operator. International Journal of
    Biometrics & Bioinformatics (IJBB), 3(6), 96.

    *Asunciones:*

    Se asume que el genoma no posee elementos repetidos, que el primer
    elemento del recorrido (la salida), no se encuentra en el genoma y es fijo.

    Args:
        task (Task): El objeto Task asociado al problema.
        ind_a (Individual): El primer individuo a cruzar.
        ind_b (Individual): El segundo individuo a cruzar.
        args (dict): Los parámetros propios del método.

    Returns:
        tuple: Un arreglo con dos individuos descendientes.

    """

    # Tomamos las variables requeridas de la tarea
    data = task.get_data()
    cost = data['cost']
    start = data['start']
    circuit = data['circuit']
    if task.get_obj_factors()[0] > 0.0:
        minim = False
    else:
        minim = True

    # Iniciamos el proceso de cruza
    gen_a = ind_a.get_raw_genome()
    gen_b = ind_b.get_raw_genome()

    # Tamaño de los genomas (todos miden lo mismo)
    size = len(gen_a)
    size_1 = size - 1

    # Creamos arreglos con elementos de gen_a y gen_b como sus llaves, y sus
    # llaves como valores, a fin de encontrarlos rápido.
    map_a = {gen_a[i]: i for i in range(size)}
    map_b = {gen_b[i]: i for i in range(size)}

    # Conjuntos que nos indican los elementos legítimos de cada hijo.
    legal_nodes_l = set(gen_a)
    legal_nodes_r = copy(legal_nodes_l)

    # Inicio de hijo izquierdo (son_l) -----------------------------------------

    # Se inicializa el genoma del futuro hijo
    son_l_gen = []

    # Se calcula el costo para el elemento apuntalado (la salida)
    cost_a = cost[start][gen_a[0]]
    cost_b = cost[start][gen_b[0]]

    # Se elige el nodo que se agregará al genoma del hijo
    if (cost_a < cost_b) != minim:  # XOR
        last_added_l = gen_b[0]
    else:
        last_added_l = gen_a[0]

    son_l_gen.append(last_added_l)

    # Se elimina de los elementos legales el elemento agregado al hijo
    legal_nodes_l.discard(last_added_l)

    # Inicio de hijo derecho (son_r) -------------------------------------------

    # Se inicializa el genoma del futuro hijo
    son_r_gen = [None for _ in range(size)]

    # Inicializamos posición
    current_index = size_1

    # Se calcula el costo para el elemento final
    cost_a = cost[gen_a[-1]][start]
    cost_b = cost[gen_b[-1]][start]

    if circuit:  # Elegimos último nodo más cercano a la salida de los padres
        if (cost_a < cost_b) != minim:  # XOR
            last_added_r = gen_b[-1]
        else:
            last_added_r = gen_a[-1]
    else:  # Elegimos último nodo más lejano a la salida de los padres
        if (cost_a > cost_b) != minim:  # XOR
            last_added_r = gen_b[-1]
        else:
            last_added_r = gen_a[-1]

    son_r_gen[current_index] = last_added_r
    # Se elimina de los elementos legales el elemento agregado al hijo
    legal_nodes_r.discard(last_added_r)
    current_index -= 1

    # Ciclo principal. Se agrega hasta que no haya que agregar
    while current_index >= 0:

        # Sección de hijo izquierdo --------

        # Buscamos el nodo legal en 'a' ---
        not_found = True
        for i in range(map_a[last_added_l] + 1, size):
            if gen_a[i] in legal_nodes_l:
                candidate_a = gen_a[i]
                not_found = False
                break

        # No se encontró nodo legal en 'a' después del último añadido
        if not_found:
            for i in gen_a:
                if i in legal_nodes_l:
                    candidate_a = i
                    break

        cost_a = cost[last_added_l][candidate_a]

        # Buscamos el nodo legal en 'b' ---
        not_found = True
        for i in range(map_b[last_added_l] + 1, size):
            if gen_b[i] in legal_nodes_l:
                candidate_b = gen_b[i]
                not_found = False
                break

        # No se encontró nodo legal en 'b' después del último añadido
        if not_found:
            for i in gen_b:
                if i in legal_nodes_l:
                    candidate_b = i
                    break

        cost_b = cost[last_added_l][candidate_b]

        # Se elige el nodo que se agregará al genoma del hijo
        if (cost_a < cost_b) != minim:  # XOR
            last_added_l = candidate_b
        else:
            last_added_l = candidate_a
        son_l_gen.append(last_added_l)

        # Se elimina de los elementos legales el elemento agregado al hijo
        legal_nodes_l.discard(last_added_l)

        # Sección de hijo derecho --------

        # Buscamos el nodo legal en 'a' ---
        not_found = True
        for i in range(map_a[last_added_r] - 1, -1, -1):
            if gen_a[i] in legal_nodes_r:
                candidate_a = gen_a[i]
                not_found = False
                break

        # No se encontró nodo legal en 'a' después del último añadido
        if not_found:
            for i in range(size_1, -1, -1):
                if gen_a[i] in legal_nodes_r:
                    candidate_a = gen_a[i]
                    break

        cost_a = cost[candidate_a][last_added_r]

        # Buscamos el nodo legal en 'b' ---
        not_found = True
        for i in range(map_b[last_added_r] - 1, -1, -1):
            if gen_b[i] in legal_nodes_r:
                candidate_b = gen_b[i]
                not_found = False
                break

        # No se encontró nodo legal en 'b' después del último añadido
        if not_found:
            for i in range(size_1, -1, -1):
                if gen_b[i] in legal_nodes_r:
                    candidate_b = gen_b[i]
                    break

        cost_b = cost[candidate_b][last_added_r]

        # Se elige el nodo que se agregará al genoma del hijo
        if (cost_a < cost_b) != minim:  # XOR
            last_added_r = candidate_b
        else:
            last_added_r = candidate_a

        son_r_gen[current_index] = last_added_r

        # Se elimina de los elementos legales el elemento agregado al hijo
        legal_nodes_r.discard(last_added_r)
        current_index -= 1

    # Se instancian los hijos
    a = ind_a.copy()
    a.set_genome_from_raw(son_l_gen)
    a.set_fitness(None)
    b = ind_b.copy()
    b.set_genome_from_raw(son_r_gen)
    b.set_fitness(None)

    return a, b


def crossover_pseudoscx(task, ind_a, ind_b, args):
    """ Hace un cruzamiento de genomas que codifican una permutación, inspirado
    en SCX.

    Esta versión no considera una matriz de costos. Los nodos son insertados
    siguiendo un esquema determinista.

    El algoritmo genera dos hijos. Uno calculado de derecha a izquierda y otro
    de izquierda a derecha.

    Se asume que el primer objetivo de la tarea asociada determina si el
    problema se maximiza o minimiza.

    Ahmed, Z. H. (2010). Genetic algorithm for the traveling salesman problem
    using sequential constructive crossover operator. International Journal of
    Biometrics & Bioinformatics (IJBB), 3(6), 96.

    *Asunciones:*

    Se asume que el genoma no posee elementos repetidos, que el primer
    elemento del recorrido (la salida), no se encuentra en el genoma y es fijo.

    Args:
        task (Task): El objeto Task asociado al problema.
        ind_a (Individual): El primer individuo a cruzar.
        ind_b (Individual): El segundo individuo a cruzar.
        args (dict): Los parámetros propios del método.

    Returns:
        tuple: Un arreglo con dos individuos descendientes.

    """

    # Iniciamos el proceso de cruza
    gen_a = ind_a.get_raw_genome()
    gen_b = ind_b.get_raw_genome()

    # Tamaño de los genomas (todos miden lo mismo)
    size = len(gen_a)
    size_1 = size - 1

    # Creamos arreglos con elementos de gen_a y gen_b como sus llaves, y sus
    # llaves como valores, a fin de encontrarlos rápido.
    map_a = {gen_a[i]: i for i in range(size)}
    map_b = {gen_b[i]: i for i in range(size)}

    # Conjuntos que nos indican los elementos legítimos de cada hijo.
    legal_nodes_l = set(gen_a)
    legal_nodes_r = copy(legal_nodes_l)

    # Inicio de hijo izquierdo (son_l) -----------------------------------------

    # Se inicializa el genoma del futuro hijo (inicia con gen_a)
    last_added_l = gen_a[0]
    son_l_gen = [last_added_l]

    # Se elimina de los elementos legales el elemento agregado al hijo
    legal_nodes_l.discard(last_added_l)

    # Inicio de hijo derecho (son_r) -------------------------------------------

    # Se inicializa el genoma del futuro hijo
    last_added_r = gen_a[-1]
    son_r_gen = [None for _ in range(size)]
    son_r_gen[-1] = last_added_r

    # Inicializamos posición
    current_index = size_1 - 1

    # Se elimina de los elementos legales el elemento agregado al hijo
    legal_nodes_r.discard(last_added_r)

    # Ciclo principal. Se agrega hasta que no haya que agregar
    source = cycle(('b', 'a'))
    while current_index >= 0:
        next_source = next(source)
        # Sección de hijo izquierdo --------

        if next_source == 'a':
            # Buscamos el nodo legal en 'a' ---
            not_found = True
            for i in range(map_a[last_added_l] + 1, size):
                if gen_a[i] in legal_nodes_l:
                    last_added_l = gen_a[i]
                    not_found = False
                    break

            # No se encontró nodo legal en 'a' después del último añadido
            if not_found:
                for i in gen_a:
                    if i in legal_nodes_l:
                        last_added_l = i
                        break
        else:
            # Buscamos el nodo legal en 'b' ---
            not_found = True
            for i in range(map_b[last_added_l] + 1, size):
                if gen_b[i] in legal_nodes_l:
                    last_added_l = gen_b[i]
                    not_found = False
                    break

            # No se encontró nodo legal en 'b' después del último añadido
            if not_found:
                for i in gen_b:
                    if i in legal_nodes_l:
                        last_added_l = i
                        break

        son_l_gen.append(last_added_l)

        # Se elimina de los elementos legales el elemento agregado al hijo
        legal_nodes_l.discard(last_added_l)

        # Sección de hijo derecho --------

        if next_source == 'a':
            # Buscamos el nodo legal en 'a' ---
            not_found = True
            for i in range(map_a[last_added_r] - 1, -1, -1):
                if gen_a[i] in legal_nodes_r:
                    last_added_r = gen_a[i]
                    not_found = False
                    break

            # No se encontró nodo legal en 'a' después del último añadido
            if not_found:
                for i in range(size_1, -1, -1):
                    if gen_a[i] in legal_nodes_r:
                        last_added_r = gen_a[i]
                        break
        else:
            # Buscamos el nodo legal en 'b' ---
            not_found = True
            for i in range(map_b[last_added_r] - 1, -1, -1):
                if gen_b[i] in legal_nodes_r:
                    last_added_r = gen_b[i]
                    not_found = False
                    break

            # No se encontró nodo legal en 'b' después del último añadido
            if not_found:
                for i in range(size_1, -1, -1):
                    if gen_b[i] in legal_nodes_r:
                        last_added_r = gen_b[i]
                        break

        son_r_gen[current_index] = last_added_r

        # Se elimina de los elementos legales el elemento agregado al hijo
        legal_nodes_r.discard(last_added_r)
        current_index -= 1

    # Se instancian los hijos
    a = ind_a.copy()
    a.set_genome_from_raw(son_l_gen)
    a.set_fitness(None)
    b = ind_b.copy()
    b.set_genome_from_raw(son_r_gen)
    b.set_fitness(None)

    return a, b


def crossover_one_point(task, ind_a, ind_b, args):
    """ Realiza un cruzamiento de dos individuos, mezclando los genomas
    aplicando un corte.

    Args:
        task (Task): El objeto Task asociado al problema.
        ind_a (Individual): El primer individuo a cruzar.
        ind_b (Individual): El segundo individuo a cruzar.
        args (dict): Los parámetros propios del método.

    Returns:
        tuple: Un arreglo con dos individuos descendientes.

    """

    # Elegimos al azar el punto de corte
    gen_a = ind_a.get_raw_genome()
    gen_b = ind_b.get_raw_genome()

    cut_point = randrange(1, len(gen_a))

    son_l_gen = gen_a[:cut_point]
    son_l_gen.extend(gen_b[cut_point:])

    son_r_gen = gen_b[:cut_point]
    son_r_gen.extend(gen_a[cut_point:])

    # Se instancian los hijos
    a = ind_a.copy()
    a.set_genome_from_raw(son_l_gen)
    a.set_fitness(None)
    b = ind_b.copy()
    b.set_genome_from_raw(son_r_gen)
    b.set_fitness(None)

    return a, b


def crossover_two_points(task, ind_a, ind_b, args):
    """ Realiza un cruzamiento de dos individuos, mezclando los genomas
    aplicando dos cortes.

    Args:
        task (Task): El objeto Task asociado al problema.
        ind_a (Individual): El primer individuo a cruzar.
        ind_b (Individual): El segundo individuo a cruzar.
        args (dict): Los parámetros propios del método.

    Returns:
        tuple: Un arreglo con dos individuos descendientes.

    """

    gen_a = ind_a.get_raw_genome()
    gen_b = ind_b.get_raw_genome()

    cut_a, cut_b = sample(range(len(gen_a)), 2)

    if cut_a > cut_b:
        cut_a, cut_b = cut_b, cut_a

    son_l_gen = gen_a[:cut_a]
    son_l_gen.extend(gen_b[cut_a:cut_b])
    son_l_gen.extend(gen_a[cut_b:])

    son_r_gen = gen_b[:cut_a]
    son_r_gen.extend(gen_a[cut_a:cut_b])
    son_r_gen.extend(gen_b[cut_b:])

    # Se instancian los hijos
    a = ind_a.copy()
    a.set_genome_from_raw(son_l_gen)
    a.set_fitness(None)
    b = ind_b.copy()
    b.set_genome_from_raw(son_r_gen)
    b.set_fitness(None)

    return a, b
