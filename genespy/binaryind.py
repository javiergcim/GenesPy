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

from .individual import Individual
from .utils import dec_to_bin


class BinaryInd(Individual):
    """ Clase para individuos con genoma binario.

    Attributes:
        _var_bits (tuple): Arreglo que indica cuantos bits usa cada variable
            en el genoma.
        _sign_bits (tuple): Arreglo que indica que variables poseen bit de
            signo.
        _precalc (tuple): Un arreglo que almacena factores que ajustan el
            valor entero codificado en cada variable a su valor flotante
            correcto.
        _struct (tuple): Un arreglo de arreglos que indican la forma en que se
            codifica cada variable almacenado en el genoma.

    """

    def __init__(self,
                 genome,
                 var_bits,
                 sign_bits,
                 precalc,
                 struct,
                 data=None,
                 fitness=None):
        """ Constructor de la clase *BinaryInd*.

        Args:
            genome (bytearray): Una lista con el genoma en su forma bruta.
            var_bits (tuple): Arreglo que indica cuantos bits usa cada variable
                en el genoma.
            sign_bits (tuple): Arreglo que indica que variables poseen bit de
                signo.
            precalc (tuple): Un arreglo que almacena factores que ajustan el
                valor entero codificado en cada variable a su valor flotante
                correcto.
            data (object): Un objeto arbitrario.
            fitness (list): Un arreglo con el fitness.

        """

        self._var_bits = var_bits
        self._sign_bits = sign_bits
        self._precalc = precalc
        self._struct = struct

        super().__init__(genome, data, fitness)

    def get_genome(self):
        """ Regresa el genoma del individuo en forma amigable.

        Returns:
            list: Una secuencia con el genoma.

        """

        nice_genome = []
        genome = self._genome
        left = 0
        for v, s, p in zip(self._var_bits, self._sign_bits, self._precalc):
            if s:  # Si tiene bit de signo
                if genome[left] == 48:  # positivo
                    nice_genome.append(int(genome[left + 1:left + v], 2) * p)
                else:  # negativo
                    nice_genome.append(-int(genome[left + 1:left + v], 2) * p)
            else:
                nice_genome.append(int(genome[left:left + v], 2) * p)

            left += v

        return nice_genome

    def set_genome(self, genome):
        """ Recibe un genoma en su forma amigable y la transforma en la forma
        cruda para ser almacenada en el individuo.

        El genoma debe ser compatible con las especificaciones establecidas en
        los atributos del indivuduo, como *_var_bits* y *_sign_bits*

        Args:
            genome (iterable): El genome en su forma amigable.

        """

        new_raw = bytearray()
        for num, params in zip(genome, self._struct):
            new_raw.extend(dec_to_bin(num, params[0], params[1], params[2]))

        self._genome = new_raw
