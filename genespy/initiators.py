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

from random import shuffle, uniform, getrandbits, choices
from .individual import Individual
from .binaryind import BinaryInd


def init_permutation_pop(n, elements):
    """ Crea una población de tamaño *n* de individuos con un genoma que
    almacena permutaciones. Los elementos a permutar se establecen
    en *elements*.

    Args:
        n (int): Cantidad de individuos a crear.
        elements (list|tuple): Un arreglo con los elementos a permutar.

    Returns:
        list: La población.

    """

    # Se forzan al menos dos individuos
    if n < 2:
        n = 2

    new_pop = []
    for _ in range(n):
        genome = list(elements[:])
        shuffle(genome)
        new_pop.append(Individual(genome))

    return new_pop


def init_float_pop(n, numbers, minimum, maximum):
    """ Crea una población de tamaño *n* de individuos con un genoma que
    almacena numberos flotantes.

    Args:
        n (int): Cantidad de individuos a crear.
        numbers (int): Cantidad de números almacenados en un genoma.
        minimum (float): Valor mínimo del rango del cual se tomarán los números.
        maximum (float): Valor máximo del rango del cual se tomarán los números.

    Returns:
        list: La población.

    """

    # Se forzan al menos dos individuos
    if n < 2:
        n = 2

    new_pop = []
    for _ in range(n):
        genome = []
        for __ in range(numbers):
            genome.append(uniform(minimum, maximum))
        new_pop.append(Individual(genome))

    return new_pop


def init_binary_pop(n, structure):
    """ Crea una población de tamaño *n* de individuos con un genoma que
    almacena variables codificadas en binario.

    Args:
        n (int): Cantidad de individuos a crear.
        structure (tuple): Un arreglo que especifica cómo se codificarán las
            variables en el genoma. Para cada variavle hay un elemento. A su
            vez, cada elemento posee otros tres, que indicarán, en este
            orden: bit de signo, bits de parte entera, bits de mantisa.

        *Ejemplo*

        Dos varables, la primera con bit de signo, diez bits para almacenar la
        parte entera, y cinco para la parte decimal. La segunda variable no
        posee signo, trece bits para la parte entera y cero para la mantisa.

        ((True, 10, 5), (False, 13, 0))

    Returns:
        list: La población.

    """

    # Se forzan al menos dos individuos
    if n < 2:
        n = 2

    # Se calculan atributos de aceleración de cálculo con base en estructura
    total_bits = 0
    var_bits = []
    sign_bits = []
    precalc = []
    for i in structure:
        current_bits = sum(i)
        total_bits += current_bits
        var_bits.append(current_bits)
        sign_bits.append(i[0])
        precalc.append(1.0 / (2**i[2]))

    # Se crean los individuos
    new_pop = []
    for _ in range(n):
        genome = bytearray(
            '{0:b}'.format(getrandbits(total_bits)).zfill(total_bits),
            'ascii')
        new_pop.append(BinaryInd(genome,
                                 tuple(var_bits),
                                 tuple(sign_bits),
                                 tuple(precalc),
                                 structure))

    return new_pop
