import json

def fetch_most_populated_countries(filename, num_countries):
    """
    Load country data from a JSON file and return 
    the top 'num_countries' based on population.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        countries = json.load(file)

    sorted_countries = sorted(countries, key=lambda country: country['population'], reverse=True)

    most_populated = [{'country': country['name'], 'population': country['population']} for country in sorted_countries[:num_countries]]

    return most_populated

filename = "countries_data.json"
print(fetch_most_populated_countries(filename, 10))
print(fetch_most_populated_countries(filename, 3))
