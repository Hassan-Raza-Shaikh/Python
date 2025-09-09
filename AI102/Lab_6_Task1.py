import json
from collections import Counter

def find_most_spoken_languages(filename, n):
    """
    Reads country data from a JSON file and returns 
    the 'n' most widely spoken languages along with their frequency.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        countries = json.load(file)

    language_frequency = Counter()
    for country in countries:
        for language in country.get('languages', []):
            language_frequency[language] += 1

    most_common_languages = language_frequency.most_common(n)

    return most_common_languages

filename = 'countries_data.json'
print(find_most_spoken_languages(filename, 10))
print(find_most_spoken_languages(filename, 3))
