# Un script de ejemplo

from genespy.task import Task
from genespy.mutators import mutate_normal
from genespy.crossovers import crossover_one_point
from genespy.selectors import select_vasconcelos
from genespy.algorithms import cos_mutation_ga
from genespy.initiators import init_float_pop


def beale(task, args):
    """ Mi función de evaluación.

    Args:
        task (Task): La tarea asociada al problema.
        args (list): Un arreglo con los argumentos codificados en el genoma.

    Returns:
        float: El fitness asociado a los argumentos proporcionados.

    """

    return (1.5 - args[0] + args[0]*args[1])**2.0 +\
           (2.25 - args[0] + args[0]*args[1]**2.0)**2.0 +\
           (2.625 - args[0] + args[0]*args[1]**3.0)**2.0


def opti_func():
    """ Ésta función prepara la tarea y ejecuta el algorítmo genético.

    """

    n = 500  # Individuos
    gen = 200  # Generaciones máximas
    cp = 0.3  # Probabilidad de cruza
    max_mp = 0.5  # Máxima probabilidad de mutación
    cycle_mp = 100.0  # Generaciónes por ciclo de mutación
    elitism = 1.0  # Porcentaje de elitismo
    duration = float('inf')  # Duración máxima en segundos
    verbose = 10  # Frecuencia de reporte

    # Se crea la tarea
    task = Task()

    # Se establece población
    the_pop = init_float_pop(n, 2, -5.0, 5)
    task.set_population(the_pop)

    # Se establecen funciones de cruza, mutacion y selección
    task.set_evals([beale], [-1.0])
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


opti_func()
