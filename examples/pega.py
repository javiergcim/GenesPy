from genespy.task import Task
from genespy.utils import create_distance_matrix, travel_cost
from genespy.mutators import mutate_insert, mutate_multiple, mutate_swap
from genespy.crossovers import crossover_scx, crossover_pseudoscx
from genespy.selectors import select_vasconcelos
from genespy.algorithms import cos_mutation_ga
from genespy.initiators import init_permutation_pop


def peg_optimize_travel(destinations, start_d='pegalinas'):
    # Creamos lista de destinos
    points_map = {}
    genome_points = []

    for key in range(len(destinations)):
        points_map[destinations[key]['id']] = key
        if destinations[key]['id'] != start_d:
            genome_points.append(destinations[key]['id'])

    # Se crean valores de configuración
    data = {'start': start_d,
            'circuit': False,
            'cost': create_distance_matrix(destinations)}
    n = 500  # Individuos
    gen = 10000  # Generaciones máximas
    cp = 0.3  # Probabilidad de cruza
    max_mp = 0.5  # Máxima probabilidad de mutación
    cycle_mp = 100.0  # Generaciónes por ciclo de mutación
    elitism = 1.0  # Porcentaje de elitismo
    verbose = 10

    # Calculamos una duración adecuada de ejecución (MAX 30 segundos):
    duration = len(destinations)**3 * .0009
    if duration <= .05:
        duration = .05
    elif duration > 30.0:
        duration = 30.0

    # Se crea la tarea
    task = Task()

    # Se establecen datos
    task.set_data(data)

    # Se establece población
    the_pop = init_permutation_pop(n, genome_points)
    task.set_population(the_pop)

    # Se establecen funciones de cruza, mutacion y selección
    task.set_evals([travel_cost], [-1.0])
    task.set_mutator(mutate_swap)
    # task.set_mutator(mutate_multiple,
    #                  {'operators': [mutate_swap, mutate_insert]})
    task.set_crossover(crossover_pseudoscx)
    task.set_selector(select_vasconcelos, {'cp': cp})

    # Inicia el algoritmo
    sol = cos_mutation_ga(task,
                          max_mp,
                          cycle_mp,
                          elitism,
                          duration,
                          gen,
                          verbose)

    return sol


destinos = [{'id': 'pegalinas', 'latitude': 19.384271, 'longitude': -99.167227},
            {'id': 'valle', 'latitude': 19.3714, 'longitude': -99.168191},
            {'id': 'luz', 'latitude': 19.388440, 'longitude': -99.220657},
            {'id': 'villada', 'latitude': 19.388132, 'longitude': -99.011080},
            {'id': 'triunfo', 'latitude': 19.37575146, 'longitude': -99.117958},
            {'id': 'lomas', 'latitude': 19.422109, 'longitude': -99.213864},
            {'id': 'arigola', 'latitude': 19.422109, 'longitude': -99.213864},
            {'id': 'indios verdes', 'latitude': 19.489285, 'longitude': -99.110390},
            {'id': 'loma linda', 'latitude': 19.459531, 'longitude': -99.244397},
            {'id': 'juarez', 'latitude': 19.429314, 'longitude': -99.153360},
            {'id': 'merced', 'latitude': 19.425649, 'longitude': -99.127991},
            {'id': 'sixflags', 'latitude': 19.300642, 'longitude': -99.206603},
            {'id': 'doctores', 'latitude': 19.415314, 'longitude': -99.145035},
            {'id': 'teotongo', 'latitude': 19.350216, 'longitude': -99.991517},
            {'id': 'satelite', 'latitude': 19.505974, 'longitude': -99.244042},
            {'id': 'campestre', 'latitude': 19.355233, 'longitude': -99.192806},
            {'id': 'ecatepec', 'latitude': 19.554727, 'longitude': -99.032422},
            {'id': 'abdías', 'latitude': 19.351077, 'longitude': -99.294937},
            {'id': 'popular', 'latitude': 19.367837, 'longitude': -99.119803},
            {'id': 'mixcoac', 'latitude': 19.375162, 'longitude': -99.183480},
            {'id': 'hipódromo', 'latitude': 19.410012, 'longitude': -99.173479},
            {'id': 'zona escolar', 'latitude': 19.540970, 'longitude': -99.150340},
            {'id': 'valle dorado', 'latitude': 19.546474, 'longitude': -99.216605},
            {'id': 'nativitas', 'latitude': 19.381869, 'longitude': -99.135589},
            {'id': 'ajusco', 'latitude': 19.317729, 'longitude': -99.159960},
            {'id': 'portales', 'latitude': 19.364219, 'longitude': -99.144475},
            {'id': 'irrigación', 'latitude': 19.439995, 'longitude': -99.208331},
            {'id': 'militar', 'latitude': 19.435463, 'longitude': -99.216742},
            {'id': 'abastos', 'latitude': 19.417994, 'longitude': -99.066741}]

solucion = peg_optimize_travel(destinos, start_d='pegalinas')
print(solucion)
