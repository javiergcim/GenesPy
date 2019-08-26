from math import floor
from genespy.task import Task
from genespy.mutators import mutate_flip
from genespy.crossovers import crossover_one_point
from genespy.selectors import select_vasconcelos, select_tournament
from genespy.algorithms import cos_mutation_ga
from genespy.initiators import init_binary_pop


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


n = 200  # Individuos
gen = 10000  # Generaciones máximas
duration = 10.0  # Duración en segundos
cp = 0.3  # Probabilidad de cruza
max_mp = 0.5  # Máxima probabilidad de mutación
cycle_mp = 100.0  # Generaciónes por ciclo de mutación
elitism = 1.0  # Porcentaje de elitismo
verbose = 10

# Se crea la tarea
task = Task()

# Se establece población
struct = ((True, 5, 5),  # x
          (True, 5, 5))  # y
the_pop = init_binary_pop(n, struct)
task.set_population(the_pop)

# Se establecen funciones de cruza, mutacion y selección
task.set_evals([beale], [-1.0])
task.set_mutator(mutate_flip, {'mp': max_mp})
task.set_crossover(crossover_one_point)
task.set_selector(select_vasconcelos, {'cp': cp})
# task.set_selector(select_tournament, {'k': floor(0.005 * n), 'matchs': floor(cp * n), 'obj_index': 0})

# Inicia el algoritmo
sol = cos_mutation_ga(task,
                      max_mp,
                      cycle_mp,
                      elitism,
                      duration,
                      gen,
                      verbose)

print(sol)
print(sol.get_genome())
