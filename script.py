import json
import argparse
from pathlib import Path
import math

parser = argparse.ArgumentParser(description="Run perf on all cache models")
parser.add_argument(
    "-d",
    "--data-file",
    type=str,
    help="JSON file containing data",
    required=True,
)

args = parser.parse_args()

def top_cities_by_country(data):
    # Group cities by country code
    countries = {}
    for entry in data:
        country_code = entry["country_code"]
        if country_code not in countries:
            countries[country_code] = []
        countries[country_code].append(entry)

    # Sort and select top 10 cities for each country
    top_cities = {}
    for country, cities in countries.items():
        sorted_cities = sorted(cities, key=lambda x: x.get("population", 0), reverse=True)
        top_cities[country] = sorted_cities[:10]

    return top_cities

# Example usage
data = json.loads(Path(args.data_file).read_text())
top_cities = top_cities_by_country(data)

# Print top cities for each country with their name, population, and coordinates
# for country, cities in top_cities.items():
#     print(f"Country: {country}")
#     for city in cities:
#         name = city["name"]
#         population = city["population"]
#         coordinates = city["coordinates"]
#         print(f"  - {name}, Population: {population}, Coordinates: ({coordinates['lat']}, {coordinates['lon']})")


import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# plt.rcParams['axes.spines.right'] = False
# plt.rcParams['axes.spines.top'] = False
# plt.rcParams['axes.spines.left'] = False
# plt.rcParams['axes.spines.bottom'] = False

def plot_cities_on_map(cities, out_file, projection=ccrs.Mercator()):
    # Initialize a plot with the Mercator projection
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': projection})
    
    # Don't add coastlines for reference
    # ax.coastlines()

    min_population = min(city["population"] for city in cities if city["population"] is not None)
    max_population = max(city["population"] for city in cities if city["population"] is not None)
    population_range = max_population - min_population

    # Plot each city
    for city in cities:
        lon = city["coordinates"]["lon"]
        lat = city["coordinates"]["lat"]
        population = city["population"] if city["population"] is not None else min_population
        # dot_size = 10 + 90 * ((population - min_population) / population_range)
        dot_size = math.log2(1 + population)

        opacity=1
        ax.plot(lon, lat, 'ko', markersize=dot_size, transform=ccrs.Geodetic(), alpha=opacity)

        # Don't annotate the city name
        # ax.text(lon + 0.5, lat + 0.5, city["name"], transform=ccrs.Geodetic())

    # Remove the border of the plot
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # original size
    plt.savefig(out_file)
    # crop image with padding
    # plt.savefig(out_file, bbox_inches='tight', pad_inches=1)
    plt.close()

print('List of countries with insufficient cities in dataset:')
for country in top_cities.keys():
# for country in ['ES']:
    cities = top_cities[country]
    if len(cities) < 10:
        print(f'{country}: only {len(cities)} cities!')
        continue
        
    plot_cities_on_map(cities, Path('images/mercator/').joinpath(f'{country}.svg'))

