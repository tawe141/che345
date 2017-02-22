import os
import pickle

from googlemaps import Client
from googlemaps.distance_matrix import distance_matrix
import dotenv

dotenv.load()


def gather(client: Client, origin: str, destinations: list) -> list:
    """
    Gathers all distances between origin and destination cities
    using Google Distance Matrix API

    :param client: Client object provided by googlemaps package
    :param origin: origin city
    :param destinations: list of destination cities
    :return: list of distances in meters in the order of list destinations
    """
    data = distance_matrix(client, origin, destinations)
    return [
        data['rows'][0]['elements'][i]['distance']['value']
        for i in range(0, len(destinations))
    ]


def left_pad(iterable: list, length: int, fill=0) -> list:
    """
    Pads with some string or float on the left of an array
    Helps generate upper-right triangular matrix

    :param iterable: iterable object (in this usage, a list)
    :param length: total length of resulting List
    :param fill: fill string for padding; defaults to ''
    :return: list padded on left with fill
    """
    return [fill] * (length - len(iterable)) + iterable if length >= len(iterable) else 0


def iter_gather(client: Client, cities: list) -> list:
    """
    Iteratively gathers distance data and
    formulates an upper triangular matrix of distances between cities

    Add list of blanks at the end to accommodate for missing city distance for last city in list

    :param client: Client object provided by googlemaps package; to be passed to gather()
    :param cities: list of city names
    :return: returns 2D upper triangular matrix of distances
    """
    return [
        left_pad(
            gather(client, cities[i], cities[(i+1):]),
            len(cities)
        ) for i in range(len(cities) - 1)
    ] + [left_pad([], len(cities))]  # last empty list accommodates for cities(-1)


def run(cities: list, force=False) -> list:
    client = Client(key=dotenv.get('API_KEY'))
    if force:
        os.remove('distance_data')
        with open('distance_data', mode='ab') as data_file:
            matrix = iter_gather(client, cities)
            pickle.dump(matrix, data_file)
            return matrix
    try:
        is_empty = os.stat('distance_data').st_size == 0
        if is_empty:
            with open('distance_data', mode='wb') as data_file:
                matrix = iter_gather(client, cities)
                pickle.dump(matrix, data_file)
                return matrix
        else:
            with open('distance_data', mode='rb') as data_file:
                return pickle.load(data_file)
    except FileNotFoundError:
        with open('distance_data', mode='ab') as data_file:
            matrix = iter_gather(client, cities)
            pickle.dump(matrix, data_file)
            return matrix
