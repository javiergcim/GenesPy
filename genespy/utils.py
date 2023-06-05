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

from sys import maxsize
from math import ceil, floor, log, sqrt, cos, sin, asin, pi, radians
from random import random


def geometric_dist(p):
    """Genera una variable aleatoria con distribución geométrica con
    probabilidad *p*.

    Args:
        p (float): Probabilidad del ensayo binomial correspondiente al proceso
            geométrico.

    Returns:
        int: Un valor que corresponde a la variable aleatoria.

    """

    if p == 1.0:
        return 1
    elif p == 0.0:
        return maxsize
    else:
        return ceil(log(1.0 - random(), 1.0 - p))


def gauss_dist(mean, sd, integer):
    """ Regresa una variable aleatoria distribuida normalmente. Si *integer*
    está establecido como verdadero, el valor se redondea al entero más próximo.

    Args:
        mean (float): La media de la distribución.
        sd (float): La desviación estándar de la distribución.
        integer (bool): Una bandera que indica si debe regresarse un valor
            entero.

    Returns:
        float|int: Un valor distribuido normalmente.

    """

    x = 1.0 - random()
    y = random()
    v = sqrt(-2.0 * log(x)) * cos(2.0 * pi * y) * sd + mean

    if integer:
        return round(v)
    else:
        return v


def dec_to_bin(num, sign, i_dig, d_dig):
    """ Convierte un número flotante a una expresión binaria de punto fijo.
    Se buscará encontrar la expresión binaria más cercana posible al número,
    aún si está fuera de rango.

    Args:
        num (float): El número a convertir.
        sign (bool): Indica si debe usarse bit de signo.
        i_dig (int): Cantidad de digitos para la parte entera.
        d_dig (int): Cantidad de digitos para la mantisa.

    Returns:
        bytearray: Un arreglo con el número codificado en binario.

    """

    max_abs_value = (2**i_dig - 1) + (2**d_dig - 1) / 2**d_dig

    # Se establece bit se signo (si existe)
    if sign:
        if num < 0.0:
            binary = bytearray(b'1')
        else:
            binary = bytearray(b'0')
    else:
        binary = bytearray(b'')

    if num < 0 and not sign:  # Debe ser cero
        binary.extend(bytearray(b'0') * (i_dig + d_dig))
    elif abs(num) >= max_abs_value:
        binary.extend(bytearray(b'1') * (i_dig + d_dig))
    else:
        abs_num = abs(num)
        numint = floor(abs_num)
        numdec = abs_num - numint

        # Se crea la parte entera
        binint = bytearray('{0:b}'.format(numint).zfill(i_dig), 'ascii')

        # Se crea la parte decimal
        numdec = floor(numdec * 2**d_dig)
        bindec = bytearray('{0:b}'.format(numdec).zfill(d_dig), 'ascii')

        # Se arma la cadena final
        binary.extend(binint)
        binary.extend(bindec)

    return binary

def euclidean_distance(a, b):
    """ Calcula la distancia euclidea entre dos puntos.
    Args:
        a (iterable): Coordenadas del primer punto.
        b (iterable): Coordenadas del segundo punto.

    Returns:
    
        (float) La distancia euclidea entre ambos puntos.

    """
    squares = 0
    for i in range(len(a)):
        squares += (a[i] - b[i]) ** 2
    
    distance = math.sqrt(squares)

    return distance

def haversine_distance(lat_from,
                       long_from,
                       lat_to,
                       long_to,
                       sphere_radius=6371000.0):
    """ Calcula la distancia entre dos puntos de la Tierra, con la fórmula
    de Haversine.

    Args:
        lat_from (float): Latitud del punto A en grados.
        long_from (float) Longitud del punto A en grados.
        lat_to (float): Latitud del punto B en grados.
        long_to (float): Longitud del punto B en grados.
        sphere_radius (float): Radio de la esfera.

    Returns:
        float: Distancia entre los puntos en la unidad de *sphere_radius*.

    """

    # Convertimos de grados a radianes
    lat_from = radians(lat_from)
    long_from = radians(long_from)
    lat_to = radians(lat_to)
    long_to = radians(long_to)

    lat_delta = lat_to - lat_from
    long_delta = long_to - long_from

    angle = 2.0 * asin(sqrt(sin(lat_delta / 2.0)**2 + cos(lat_from) *
                            cos(lat_to) * sin(long_delta / 2.0)**2))

    return angle * sphere_radius


def create_distance_matrix(points, euclidean = False):
    """ Crea la matriz de distancias entre un conjunto de puntos, dados de la
    forma:

    {'id': id, latitude': lat, 'longitude': long}

    Args:
        points (list): Un arreglo con los puntos a calcular sus distancias.
        euclidean (bool): Indica si la distancia se calculará de forma cartesiana.

    Returns:
        list: Una matriz cuadrada con las distancias entre los puntos.

    """

    # Creamos lista de destinos
    points_map = {}
    i = 0

    for i in range(len(points)):
        points_map[points[i]['id']] = i

    # Inicializamos la primer dimensión de la 'matriz'
    matrix = {}
    for value in points:
        matrix[value['id']] = {}

    # Calculamos los costos
    for value_from in points:
        key_from = value_from['id']
        for value_to in points:
            key_to = value_to['id']

            if key_from == key_to:
                matrix[key_from][key_to] = 0.0
                break

            if euclidean:
                matrix[key_from][key_to] = euclidean_distance(
                    points[points_map[key_from]]['coords'],
                    points[points_map[key_to]]['coords']
                )
            else:
                matrix[key_from][key_to] = \
                    haversine_distance(points[points_map[key_from]]['latitude'],
                                    points[points_map[key_from]]['longitude'],
                                    points[points_map[key_to]]['latitude'],
                                    points[points_map[key_to]]['longitude'])

            matrix[key_to][key_from] = matrix[key_from][key_to]

    return matrix


def travel_cost(genome, data):
    """ Costo de un viaje del tipo *agente viajero*.

    Args:
        genome (list): El genoma a evaluar.
        data (object): Un objeto arbitrario.


    Returns:
        float: La evaluación del individuo.

    """

    matrix = data['cost']
    cost = matrix[data['start']][genome[0]]

    for i in range(len(genome) - 1):
        cost += matrix[genome[i]][genome[i + 1]]

    if data['circuit']:
        cost += matrix[genome[-1]][data['start']]

    return cost
