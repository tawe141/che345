from googlemaps import Client
from googlemaps.distance_matrix import distance_matrix
import dotenv, pprint

dotenv.load()

pp = pprint.PrettyPrinter(indent=4)

cities = [
    "Chicago, IL",
    "Denver, CO",
    "Milwaukee, WI",
    "Indianapolis, ID",
    "Kansas City, MO",
    "St. Louis, MO"
    ]


def gather(client, origin, destinations):
    data = distance_matrix(client, origin, destinations)
    return {
        'origin': origin,
        'distances': [
                [
                    destinations[i],
                    data['rows'][0]['elements'][i]['distance']['value']
                ]
                for i in range(0, len(destinations))
            ]
    }


def iter_gather(client, cities):
    return [gather(client, cities[i], cities[:i] + cities[(i+1):]) for i in range(len(cities))]


if __name__ == '__main__':
    client = Client(key=dotenv.get('API_KEY'))
    pp.pprint(iter_gather(client, cities))