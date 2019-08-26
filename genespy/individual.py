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

from copy import copy


class Individual:
    """ Clase base para los individuos.

    Attributes:
        _genome (list|byterray): El genoma del individuo.
        _fitness (list): Un arreglo de valores fitness.
        _data (object): Un objeto arbitraria que contiene datos adjuntos al
            individuo

    """

    def __init__(self, genome, data=None, fitness=None):
        """ Constructor de la clase  *Individual*.

        Args:
            genome (list|bytearray): Una lista con el genoma en su forma bruta.
            data (object): Una objeto aritrario.
            fitness (list): Un arreglo con el fitness.

        """

        self._genome = genome
        self._fitness = fitness
        self._data = data

    def __str__(self):
        """ La representación en cadena del objeto.

        Return:
            str: La representación en cadena del individuo.

        """

        if self._genome is None:
            gen = '(none)'
        else:
            gen = str(self._genome)

        if self._fitness is None:
            fit = '(none)'
        else:
            fit = str(self._fitness)

        if self._data is None:
            data = '(none)'
        else:
            data = str(self._data)

        return ''.join(('Genome: ',
                        gen,
                        '\n',
                        'Fitness: ',
                        fit,
                        '\n',
                        'Data: ',
                        data,
                        '\n'))

    def __repr__(self):
        """ La representación en cadena del objeto.

        Return:
            str: La representación en cadena del individuo.

        """

        if self._genome is None:
            gen = '(none)'
        else:
            gen = repr(self._genome)

        if self._fitness is None:
            fit = '(none)'
        else:
            fit = repr(self._fitness)

        if self._data is None:
            data = '(none)'
        else:
            data = repr(self._data)

        return ''.join(('Genome: ',
                        gen,
                        '\n',
                        'Fitness: ',
                        fit,
                        '\n',
                        'Data: ',
                        data,
                        '\n'))

    def copy(self):
        """ Regresa una copia ligera del objeto.

        Returns:
            Individual: Una copia del objeto.

        """

        c = copy(self)
        c._genome = self._genome[:]

        return c

    def get_genome(self):
        """ Regresa el genoma del individuo en forma amigable.

        Returns:
            list: Una secuencia con el genoma.

        """

        return self._genome

    def get_raw_genome(self):
        """ Regresa el genoma del individuo en forma bruta.

        Returns:
            list: Una secuencia con el genoma.

        """

        return self._genome

    def set_genome(self, genome):
        """ Establece el genoma desde una versión amigable del mismo.

        Args:
            genome (list): Un arreglo con el genoma en forma decodificada o
                amigable.

        """

        self._genome = genome

    def set_genome_from_raw(self, genome):
        """ Establece el genoma desde una versión en bruto del mismo.

        Args:
            genome (list): Un arreglo con el genoma en bruto, tal cual es
                almacenado en el individuo.

        """

        self._genome = genome

    def get_fitness(self, i=None):
        """ Regresa el fitness del individuo.

        Regresa el arreglo de *fitness*.

        Returns:
            list: Una secuencia con el fitness elegido.

        """
        if i is None:
            return self._fitness
        else:
            return self._fitness[i]

    def set_fitness(self, fit):
        """ Establece el fitness del individuo.

        Args:
            fit (list): Un arreglo con el fitness del individuo.

        """

        self._fitness = fit

    def get_data(self):
        """ Regresa los datos arbitrarios asociados al individuo.

        Returns:
            object: Devuelve los datos arbitrarios asociados al individuo.

        """

        return self._data

    def set_data(self, data):
        """ Establece los datos arbitrarios asociados al individuo.

        Args:
            data (object): Una objeto arbitrario que se asignará al individuo.

        """

        self._data = data

    def get_size(self):
        """ Regresa la longitud del genoma.

        Returns:
            int: La longitud del genoma.

        """

        return len(self._genome)
