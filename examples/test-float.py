# Un script de ejemplo

from genespy.task import Task
from genespy.mutators import mutate_normal
from genespy.crossovers import crossover_one_point
from genespy.selectors import select_vasconcelos
from genespy.algorithms import cos_mutation_ga
from genespy.initiators import init_float_pop


def example_evaluation_function(genome, data):
    """ Función de evaluación de ejemplo.

    Args:
        genome (list): Un arreglo con los argumentos codificados en el genoma.
        data (object): Un objeto arbitrario asociado al problema.

    Returns:
        float: El fitness asociado a los argumentos proporcionados.

    """

    return (1.5 - genome[0] + genome[0] * genome[1]) ** 2.0 + \
           (2.25 - genome[0] + genome[0] * genome[1] ** 2.0) ** 2.0 + \
           (2.625 - genome[0] + genome[0] * genome[1] ** 3.0) ** 2.0


def my_example():
    """ Esta función prepara la tarea y ejecuta el algoritmo genético.

    """

    n = 500  # Individuos
    gen = 400  # Generaciones máximas
    cp = 0.3  # Probabilidad de cruza
    max_mp = 0.5  # Máxima probabilidad de mutación
    cycle_mp = 100.0  # Generaciónes por ciclo de mutación
    elitism = 1.0  # Porcentaje de elitismo
    duration = float('inf')  # Duración máxima en segundos
    verbose = 10  # Frecuencia de reporte

    # Se crea la tarea
    task = Task()

    # Se crea y asigna la población inicial
    # (individuals, number of genes, min random value, max random value)
    the_pop = init_float_pop(n, 2, -5.0, 5)
    task.set_population(the_pop)

    # Se establecen funciones de cruza, mutacion y selección
    task.set_evals([example_evaluation_function], [-1.0])
    task.set_mutator(mutate_normal, {'mp': max_mp, 'sd': 0.5, 'integer': False})
    task.set_crossover(crossover_one_point)
    task.set_selector(select_vasconcelos, {'cp': cp})

    # Inicia el algoritmo
    sol = cos_mutation_ga(task,
                          max_mp,
                          cycle_mp,
                          elitism,
                          duration,
                          gen,
                          verbose)

    print(sol)
    print('Genome only:', sol.get_genome())


my_example()
