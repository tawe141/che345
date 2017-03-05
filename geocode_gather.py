import pickle

import googlemaps as gmaps
import googlemaps.geocoding as geocoding
import dotenv

dotenv.load()


def get_geocode(client, city: str) -> tuple:
    data = geocoding.geocode(client, city)
    return data[0]['geometry']['location']['lng'], data[0]['geometry']['location']['lat']


def run(cities):
    try:
        with open('coordinates_data', 'r+b') as data_file:
            data = pickle.load(data_file)
            if len(cities) != len(data):
                client = gmaps.Client(dotenv.get('GEOCODING_API_KEY'))
                print('Generating coordinate data...')
                data = {cities.index(c): get_geocode(client, c) for c in cities}
                file_bytes = pickle.dumps(data)
                data_file.seek(0)
                data_file.write(file_bytes)
                data_file.truncate()
            return data

    except FileNotFoundError:
        client = gmaps.Client(dotenv.get('GEOCODING_API_KEY'))
        print('Generating coordinate data...')
        data = {cities.index(c): get_geocode(client, c) for c in cities}
        with open('coordinates_data', 'ab') as data_file:
            pickle.dump(data, data_file)
            return data
