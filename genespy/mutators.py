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

from random import randrange
from .utils import geometric_dist, gauss_dist


def mutate_swap(task, individual, args):
    """ Muta el individuo proporcionado in-situ, intercambiando de posición dos
    elementos de sus genomas cada vez. La cantidad de parejas intercambiadas
    estará en función de la probabilidad *mp*.

    Establece en *None* el fitness del individuo mutado.

    Args:
        task (Task): Una referencia a la tarea asociada al elemento (no usada).
        individual (Individual): Un individuo.
        args (dict): Un arreglo con los parámetros propios de este método. *mp'*
        como un número entre 0.0 y 1.0, que representa la probabilidad de que un
        elemento de $genome sea escogido para ser intercambiado por otro.

    """

    mp = args['mp']
    gen = individual.get_raw_genome()
    max_i = len(gen)

    j = geometric_dist(mp) - 1  # Primer j (y nodo a intercambiar)
    while j < max_i:
        # Elegimos al azar el nodo k
        k = randrange(max_i)

        # Intercambiamos j y k
        gen[j], gen[k] = gen[k], gen[j]

        j += geometric_dist(mp)

    individual.set_fitness(None)


def mutate_flip(task, individual, args):
    """ Muta el individuo proporcionado in-situ, intercambiando el valor de
    una posición del genoma de 0 a 1, o visceversa (sólo para genomas binarios).
    La elección del bit a cambiar se hace con probabilidad *mp*.

    Establece en *None* el fitness del individuo mutado.

    Args:
        task (Task): Una referencia a la tarea asociada al elemento (no usada).
        individual (Individual): Un individuo.
        args (dict): Un arreglo con los parámetros propios de este método. *mp'*
        como un número entre 0.0 y 1.0, que representa la probabilidad de que un
        elemento de $genome sea escogido para ser intercambiado por otro.

    """

    mp = args['mp']
    gen = individual.get_raw_genome()
    max_i = len(gen)

    j = geometric_dist(mp) - 1  # Primer j (y nodo a intercambiar)
    while j < max_i:
        if gen[j] == 48:
            gen[j] = 49
        else:
            gen[j] = 48

        j += geometric_dist(mp)

    individual.set_fitness(None)


def mutate_insert(task, individual, args):
    """ Muta el individuo proporcionado in situ. Divide el genoma en tres
    subarreglos A, B, C. El operador hace al genoma A, C, B.

    Establece en *None* el fitness del individuo mutado.

    Args:
        task (Task): Una referencia a la tarea asociada al elemento (no usada).
        individual (Individual): Un individuo.
        args (dict): Un arreglo con los parámetros propios de este método
            (no usados).

    """

    gen = individual.get_raw_genome()

    max_i = len(gen)
    a = randrange(max_i)
    b = randrange(max_i)

    if b < a:
        a, b = b, a

    slice_a = gen[:a]
    slice_b = gen[a:b]
    slice_c = gen[b:]

    slice_a.extend(slice_c)
    slice_a.extend(slice_b)

    individual.set_genome_from_raw(slice_a)
    individual.set_fitness(None)


def mutate_multiple(task, individual, args):
    """ Muta el individuo proporcionado in situ, elige al azar un operador de
    mutación de los especificados en la inicialización. Los parámetros de para
    cada operador de mutación se especificaron en la inicialización.

    Establece en *None* el fitness del individuo mutado.

    """

    operator_index = randrange(len(args['operators']))
    args['operators'][operator_index](task, individual, args)


def mutate_normal(task, individual, args):
    """ Muta el individuo proporcionado in situ, alterando de forma normal los
    valores de los genes elegidos al azar en el genoma.

    Establece en *None* el fitness del individuo mutado.

    Args:
        task (Task): Una referencia a la tarea asociada al elemento (no usada).
        individual (Individual): Un individuo.
        args (dict): Un arreglo con los parámetros propios de este método.
            *mp* como la probabilidad de que un gen sea mutado, *sd* como la
            desviación estándar aplicada a la mutación, *integer*, si se desea
            que los valores que se establezcan en el genoma sean enteros.

    """

    mp = args['mp']
    sd = args['sd']
    integer = args['integer']
    gen = individual.get_raw_genome()
    max_i = len(gen)

    j = geometric_dist(mp) - 1  # Primer j (y nodo a intercambiar)
    while j < max_i:
        mean = gen[j]
        gen[j] = gauss_dist(mean, sd, integer)

        j += geometric_dist(mp)

    individual.set_fitness(None)
