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
from random import randrange, sample
from .individual import Individual


class Task:
    """ Clase base para las tareas.

    Attributes:
        _population (list): La coleción de individuos de la población.
        _current_gen (int):  Indica la generacion actual cuando se está
            aplicando un algoritmo genético sobre la tarea.
        _desired_size (int): La cantidad de individuos deseada para la población
            (la población puede tener una cantidad diferente de elementos en
            algunos momentos).
        _target_obj (list): Es un arreglo de índices de objetivos, que se
            usará para las comparaciones y ordenamiento de los individuos de la
            población.
        _constraints (list): Un arreglo con las funciones que harán las veces de
            restricciones. Para cada función una restricción. Las
            restricciones se evalúan siempre antes que los objetivos. Sólo si se
            cumplen todas las restricciones, se evalúan posteriormente por las
            funciones objetivo. Las funciones de restricción deben regresar 0 si
            se cumple la condición, 1 en caso de fallo.
        _penalties (list): Arreglo de penalizaciones máximas aplicadas a un
            individuo que no cumple las restricciones establecidas por el
            usuario. Debe tener tantos elementos como funciones objetivo tenga
            la tarea.
        _mutator (func): La función que hará las veces de mutador.
        _mutator_args (dict): Parámetros para la función de mutación.
        _crossover (func): La función de cruzamiento.
        _crossover_args (dict): Parámetros para la función de cruzamiento.
        _selector (func): La función selector. Ésta función aplicará la función
            de cruzamiento a las parejas de individuos seleccionadas, y guardará
            los resultados en la población.
        _selector_args (dict): Parámetros para la función de selección.
        _objectives (list): Arreglo con las funciones de evaluación. Una para
            cada objetivo.
        _obj_factors (list): Arreglo con la ponderación de cada función
            objetivo. Un elemento para cada una.
        _data (object): Un objeto arbitrario asociado a la Tarea, con datos
            proclives a ser usados por algún algoritmo de cruzamiento,
            selección o mutación.

    """

    def __init__(self):
        """ Constructor de la clase  *Task*.

        """

        self._population = None
        self._current_gen = None
        self._desired_size = None
        self._target_obj = []
        self._constraints = []
        self._penalties = []
        self._mutator = None
        self._mutator_args = {}
        self._crossover = None
        self._crossover_args = {}
        self._selector = None
        self._selector_args = {}
        self._objectives = []
        self._obj_factors = []
        self._data = None

    def get_population(self):
        """ Regresa la población actual de la tarea.

        Returns:
            list: Un arreglo con la población actual.

        """

        return self._population

    def get_subpopulation_copy(self, the_slice):
        """ Regresa una copia de un corte de la población.

        Args:
            the_slice (slice): Un corte que representa el subconjunto de la
                población deseada.

        Returns:
            list: Un arreglo con la copia de los elementos seleccionados.

        """

        sub = self._population[the_slice]

        for i in range(len(sub)):
            sub[i] = sub[i].copy()

        return sub

    def replace_population(self, pop):
        """ Reemplaza la población actual. Ésta función no ajusta el tamaño
        deseable de la población. Para ello, usar set_population.

        Args:
            pop (list): Un arreglo con la población que reemplaza la anterior.

        """

        self._population = pop

    def set_population(self, pop):
        """ Establece la población actual. En el proceso se actualiza el tamaño
        deseable de la población.

        Args:
            pop (list):  Un arreglo con la población que reemplaza la anterior.

        """

        self._population = pop
        self._desired_size = len(pop)

    def append_population(self, pop, first=False):
        """ Agrega individuos a la población actual. Ésta función no actualiza
        la cantidad de individuos deseada de la población.

        Args:
            pop (list): Un arreglo con la población que se añadirá a la
                actual.
            first (bool): Indica si los individuos que se añaden van al inicio
                del arreglo.

        """

        if first:
            self._population = pop + self._population
        else:
            self._population.extend(pop)

    def adjust_population_size(self, n=None):
        """ Ajusta la población para que contenga la cantidad de elementos
        especificado en el atributo *_desired_size* de la instancia, o bien, la
        indicada explícitamente como argumento. Si se indica explícitamente,
        el núevo tamaño será establecido como el tamaño *deseado* de la
        población.

        Modifica la población in-situ.

        La población crecerá o será truncada según corresponda.

        Si es truncada, los últimos *n - _desired_size* elementos del arreglo
        son eliminados.

        Si es expandida, los nuevos individuos serán generados mutando con una
        probabilidad aleatoria elementos elegidos al azar en la población.
        Se anexan al final del arreglo.

        Se asume que hay una función de mutación establecida, se aplican los
        argumentos de dicho operador en ese momento.

        Args:
            n (int): Cantidad de elementos que debe poseer la población.

        Returns:
            bool: Regresa verdadero si la población creció. Falso si se redujo o
                quedó igual.

        """

        pop = self._population
        current_size = len(pop)

        # Se ajusta o no el atributo _desired_size, y se establece n final
        if n is None:
            n = self._desired_size
        else:
            self._desired_size = n

        diff = n - current_size

        # Se debe truncar o dejar igual. Elegimos al azar (sin sesgo)
        if diff <= 0:
            re_evaluate = False
            selected = [0]
            selected.extend(sorted(sample(range(1, current_size),
                                     n)))  # Orden original
            reduced_pop = []
            for i in selected:
                reduced_pop.append(pop[i])

            self.replace_population(reduced_pop)

        else:  # Se deben añadir elementos
            re_evaluate = True
            mutator_args = self._mutator_args
            while diff:
                # Se elige un elemento al azar de la población, y se clona
                index = randrange(current_size)
                born = pop[index].copy()

                # Se crea nuevo genoma de mutación
                self._mutator(self, born, mutator_args)

                # Se añade a la población
                pop.append(born)

                diff -= 1

        return re_evaluate

    def remove_duplicate_fitness(self):
        """
        Returns:Elimina los elementos con fitness duplicado. Está función no
        ajusta el cantidad de individuos deseados en la población.

        """

        self.order_population()
        real_size = len(self._population)

        new_population = [self._population[0]]
        current_fit = new_population[0].get_fitness()
        for i in range(1, real_size):
            new_fit = self._population[i].get_fitness()
            if current_fit != new_fit:
                new_population.append(self._population[i])
                current_fit = new_fit

        self._population = new_population

    def get_size(self):
        """ Regresa el número de individuos que realmente hay la población.

        Returns:
            int: El número de elementos en la población.

        """

        if self._population:
            return len(self._population)
        else:
            return 0

    def get_desired_size(self):
        """ Regresa el número de individuos que deseamos en la población.

        Returns:
            int: El número de elementos deseados en la población.

        """

        return self._desired_size

    def set_generation(self, g):
        """ Establece la generación actual en la que se encuentra la tarea, si
        se está ejecuando un algoritmo genético.

        Args:
            g (int|None): La generacion actual. *None* si no hay algoritmo
                activo.

        """
        self._current_gen = g

    def get_generation(self):
        """ Regrese la generación actual en la que se encuentra la tarea, si se
        está ejecuando un algoritmo genético.

        Returns:
            int|None: La generacion actual (de existir).

        """
        return self._current_gen

    def _individual_order_key(self, a):
        """ Regresa un arreglo que servirá como llave para una función de
        ordenación sort o sorted al momento de ordenar objetos de tipo
        Individual.

        Se utiliza el atributo *_target_obj* como el indicador de que objetivos,
        y en que orden, se deberán emplear para la comparación por una función
        de ordenamiento o comparación.

        Si el individuo no posee fittnes, se forzará una tupla
        con float('inf').

        Args:
            a (Individual): Un individuo.

        Returns:
            list: Un arreglo que servirá de llave para ordenar individuos.

        """
        a_fit = a.get_fitness()

        if a_fit is None:
            a_fit = [float('inf') for _ in range(len(self._obj_factors))]
        else:
            a_fit = a_fit[:]

        # Cambiamos signos según se minimiza o maximiza
        for i in range(len(a_fit)):
            if self._obj_factors[i] > 0.0:
                a_fit[i] = -a_fit[i]

        # Ordenamos según _target_obj
        disc = []
        for i in self._target_obj:
            disc.append(a_fit[i])

        return disc

    def order_population(self, objectives=None):
        """ Ordena una población con base del fitness del objetivo seleccionado.
        La función siempre colocará los elementos más favorables según el orden
        establecido en el arreglo dado como parámetro, que será una lista de los
        índices de las funciones objetivo a considerar.

        Si no se provee de objectives, se priorizarán los objetivos tal y como
        fueron registrados en la tarea. La tarea debe tener definidas, al menos,
        las funciones objetivo.

        El cambio de la población es in-situ.

        Args:
            objectives (iterable|None): Un arreglo con los índices de los
                objetivos.
            que deberán tomarse en cuenta, y en que orden, para la ordenación.

        """
        if objectives is None:
            objectives = tuple(range(len(self._obj_factors)))
        self._target_obj = tuple(objectives)
        self._population.sort(key=self._individual_order_key)

    def get_individual(self, i):
        """ Regresa el individuo de la población especificado.

        Args:
            i (int): El índice del individuo deseado.

        Returns:
            Individual: El individuo seleccionado.

        """

        return self._population[i]

    def set_evals(self, evals, factors):
        """ Función que permite asociar las funciones de evaluación de problema,
        que se provee con *evals*.

        Para cada objetivo se utiliza un valor de ponderación, que se provee
        con *factors*. Útil para los problemas multiobjetivo.

        Si el valor en *factors* es positivo, se considera un problema de
        maximización, si es negativo se considera de minimización.

        Args:
            evals (iterable): Arreglo con los nombres completamente cualificados
                de las funciones que se utilizarán para evaluar un individuo.
            factors (iterable): Arreglo con los valores de ponderación asociados
                a cada función de evaluación. Si el valor es positivo, se
                considera un problema de maximización, si es negativo se
                considera de minimización. Debe ser del mismo tamaño que
                *evals*.

        """
        try:
            if len(evals) == len(factors):
                self._objectives = tuple(evals)
                self._obj_factors = tuple(factors)
            else:
                raise ValueError()
        except ValueError:
            print("Both arguments must be the same size")

    def get_obj_factors(self, i=None):
        """ Regresa el arreglo con las ponderaciones de las funciones de
        evaluación, o bien, la ponderación especificada.

        Args:
            i (int|None): El índice de la ponderación deseada.

        Returns:
            float|list: El arreglo con las ponderaciones.

        """
        if i is None:
            return self._obj_factors
        else:
            return self._obj_factors[i]

    def set_constraints(self, constraints, max_penalties):
        """ Función que permite asociar funciones que evalúan si un individuo
        cumple restricciones especificadas por el usuario.

        Así mismo, permite establecer un arreglo de valores de penalización
        máximos. Uno para cada función objetivo.

        Args:
            constraints (list): Una lista de funciones que fungirán como
                restricciones. Las funciones deben regresar 0 en caso de
                cumplirse la condición, y 1 en caso contrario.
            max_penalties: (list): Arreglo con los valores de penalización
                máxima. Uno para cada función objetivo. Deben existir tantos
                valores de penalización como funciones objetivo en la tarea.

        """

        n_penalties = len(max_penalties)
        n_constraints = len(constraints)

        try:
            if n_penalties == len(self._objectives):
                self._constraints = tuple(constraints)
                self._penalties =\
                    tuple(penalty / n_constraints for penalty in max_penalties)
            else:
                raise ValueError('max_penalities must have as many elements ' +
                                 'as objectives have the task')
        except ValueError as error:
            print(error.args[0])

    def set_mutator(self, mutator, args=None):
        """ Establece la función de mutación que se aplicará a los individuos.

        La función debe ser capaz de recibir tres parámetros: una referencia al
        objeto Task asociado, una referencia al individuo a mutar, y un
        diccionario de argumentos. Debe modificar el genoma del individuo
        proporcionado in-situ.

        Args:
            mutator (func): La función de mutación.
            args (dict): Un diccionario con los argumentos de la función de
                mutación.
        """

        if args is None:
            args = {}
        self._mutator = mutator
        self._mutator_args = args

    def set_mutator_arg(self, key, value):
        """ Establece el argumento indicado para la función de mutación.

        Args:
            key (object): La llave o nombre del argumento.
            value (object): El valor del argumento.

        """

        self._mutator_args[key] = value

    def set_crossover(self, crossover, args=None):
        """ Establece la función de cruza que se aplicará a los individuos.

        La función debe ser capaz de recibir tres parámetros: una referencia al
        objeto Task asociado, una referencia para cada individuo a cruzar (2).
        Debe generar un arreglo con los individuos nuevos como descendencia.

        El número de descendientes se asume como dos.

        Args:
            crossover (func): La función de cruza.
            args (dict): Un diccionario con los argumentos de la función de
                cruza.
        """

        if args is None:
            args = {}
        self._crossover = crossover
        self._crossover_args = args

    def set_crossover_arg(self, key, value):
        """ Establece el argumento indicado para la función de cruza.

        Args:
            key (object): La llave o nombre del argumento.
            value (object): El valor del argumento.

        """

        self._crossover_args[key] = value

    def set_selector(self, selector, args=None):
        """ Establece la función de selección que se aplicará a la población.

        La función debe ser capaz de recibir dos parámetros: una referencia al
        objeto Task asociado, y una probabilidad de cruzamiento. Debe ejecutar
        la función de cruzamiento asignada a la tarea, e incorporar la prole
        generada a la población.

        Debe modificar la población in-situ.

        Args:
            selector (func): La función de cruza.
            args (dict): Un diccionario con los argumentos de la función de
                selección.
        """

        if args is None:
            args = {}
        self._selector = selector
        self._selector_args = args

    def set_selector_arg(self, key, value):
        """ Establece el argumento indicado para la función de selección.

        Args:
            key (object): La llave o nombre del argumento.
            value (object): El valor del argumento.

        """

        self._selector_args[key] = value

    def set_data(self, data):
        """ Establece los datos arbitrarios asociados a la tarea.
        Args:
            data (object): Datos arbitrarios asociados a la tarea.

        """

        self._data = data

    def get_data(self):
        """ Obtiene los datos arbitrarios asociados a la tarea.

        Returns:
            object: Los datos arbitrarios asociados a la tarea.

        """

        return self._data

    def evaluate(self):
        """ Evalua los individuos de la población que no posean un fitness. La
        evaluación se efectúa para todas las funciones de evaluación asociadas a
        la tarea.
        
        """

        data = self._data

        for son in self._population:  # Para cada individuo
            if son.get_fitness() is None:  # No tiene fitness calculado
                fit = []
                son_genome = son.get_genome()

                # Calculamos las restricciones
                failed = 0
                for constrain in self._constraints:
                    failed += constrain(son_genome, data)

                if not failed:  # Calculamos objetivos si cumple restric.
                    for objective in self._objectives:
                        fit.append(objective(son_genome, data))
                else:  # Aplicamos penalización si no cumple restricciones
                    for penalty in self._penalties:
                        fit.append(penalty * failed)

                son.set_fitness(fit)

    def mutate(self):
        """ Aplica la función de mutación a todos los individuos de la
        población.

        """

        mutator_args = self._mutator_args
        for ind in self._population:
            self._mutator(self, ind, mutator_args)

    def apply_selection(self):
        """ Aplica la selección y cruza especificados.

        """

        self._selector(self, self._selector_args)

    def apply_crossover(self, ind_a, ind_b):
        """ Aplica el cruzamiento.

        Returns:
            tuple: Una tupla con los dos descendientes.

        """

        return self._crossover(self, ind_a, ind_b, self._crossover_args)
