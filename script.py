import json
import argparse
from pathlib import Path

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
for country, cities in top_cities.items():
    print(f"Country: {country}")
    for city in cities:
        name = city["name"]
        population = city["population"]
        coordinates = city["coordinates"]
        print(f"  - {name}, Population: {population}, Coordinates: ({coordinates['lat']}, {coordinates['lon']})")


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

    # Plot each city
    for city in cities:
        lon = city["coordinates"]["lon"]
        lat = city["coordinates"]["lat"]
        ax.plot(lon, lat, 'ko', transform=ccrs.Geodetic())

        # Don't annotate the city name
        # ax.text(lon + 0.5, lat + 0.5, city["name"], transform=ccrs.Geodetic())

   # Remove the border of the plot
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()

for country, cities in top_cities.items():
    print(cities)
    plot_cities_on_map(cities, Path('images/mercator/').joinpath(f'{country}.svg'))
