import csv


def full_data() -> dict:
    """
    Takes in a list of city names and constructs dict of tuples
    Keys are city names
    Tuples are of form (gas price, hotel price) for each city

    :rtype: dict
    """
    with open('price_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            if i == 0:
                # awful refining city names...
                cities = [i.replace('\",', '').replace('\"', '') for i in row]
            elif i == 1:
                gas = [float(i) for i in row]
            elif i == 2:
                hotel = [float(i) for i in row]
            i += 1
        return {cities[k]: (gas[k], hotel[k]) for k in range(len(cities))}


def subset(cities, data: dict) -> dict:
    return {cities.index(k): v for k, v in data.items() if k in cities}


def run(cities: list) -> dict:
    """
    Uses list of cities and gathers gas and AirBnb data for each city
    Returns dictionary of the form {city_index: (gas_price, hotel_price)}

    :param cities: list
    :return: dictionary of gas + hotel prices
    """
    return subset(cities, full_data())


