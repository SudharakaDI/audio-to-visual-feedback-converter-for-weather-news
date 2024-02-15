import spacy
import re
import requests
import json
import geopandas as gpd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

nlp = spacy.load("en_core_web_sm")

#list of locations, weather conditions, times
provinces = ["Central", "Eastern", "North-Central", "Northern","North-Western","Sabaragamuwa","Southern","Uva","Western"]
districts = ["Ampara","Anuradhapura","Badulla","Batticaloa","Colombo","Galle","Gampaha","Hambantota","Jaffna","Kalutara","Kandy","Kegalle","Kilinochchi","Kurunegala","Mannar","Matale","Matara","Moneragala","Mullaitivu","Nuwara Eliya","Nuwara-Eliya","Polonnaruwa","Puttalam","Ratnapura","Trincomalee","Vavuniya"]
weather_conditions = ["shower", "flood", "cyclone", "misty", "cloudy", "sunny", "thunder", "wind"]
times = ["morning", "afternoon", "evening", "night"]
# Define icon paths for each weather condition
icon_paths = {
    'shower': 'weatherConditionsImages/rain.png',
    'flood': 'weatherConditionsImages/flood.png',
    'cyclone': 'weatherConditionsImages/cyclone.webp',
    'misty': 'weatherConditionsImages/misty.png',
    'cloudy': 'weatherConditionsImages/cloudy.png',
    'wind': 'weatherConditionsImages/cloudy.png',
    'sunny': 'weatherConditionsImages/sunny.webp',
    'thunder': 'weatherConditionsImages/thunder.png'

}

#example sentences
sentence1 = "Showers will occur at times in Eastern, north-western, Northern and Uva provinces and several spells of showers will occur in North-central province, showers or thundershowers will occur at several places in other areas of the island after 1.00 p.m, Heavy showers about 100 mm are likely at some places in Western, Sabaragamuwa and Central provinces and in Galle and Matara districts."
sentence2 = "Misty conditions can be expected at some places in Central, Sabaragamuwa and Western provinces and showers will be occurred in Galle and Matara districts during the morning."
sentence3 = """Several spells of showers will occur in Eastern and Uva provinces and in Polonnaruwa, Matale and Nuwara-Eliya districts.
A few thundering may occur in Northern province and in Anuradhapura district.
Showers or thundershowers may occur ata few places in Western and Sabaragamuwa provinces and in Galle and Matara districts after 2.00 p.m.
Fairly strong sunny whether about (30-40) kmph can be expected at times in eastern slopes of the central hills and in Northern, North-Central, Southern,North-western, Uva and Eastern provinces.
Misty conditions can be expected at some places in Western and Sabaragamuwa provinces and in Galle and Matara districts during the morning."""
sentence4 = "Showers may occur in Western and Sabaragamuwa after 2.00 p.m. winds about (30-40) kmph in eastern slopes of the central hills."

def extract_all_entities(sentence, districts, provinces):
    sentence = sentence.replace(',', ' ') # Remove commas from the sentence
    sentence = sentence.replace('(', '').replace(')', '')
    words = sentence.split() # Split the sentence into words
    entities = []
    i = 0
    while i < len(words):
        word = words[i]
        lowercase_word = word.lower()
        doc = nlp(lowercase_word)
        lemmatized_word = doc[0].lemma_
        # Check if the word is a district or province
        if lowercase_word in [district.lower() for district in districts] or lowercase_word in [province.lower() for province in provinces]:
            # Check if the next word (if exists) combines with the current word to form a compound location name
            if i < len(words) - 1:
                combined_word = f"{lowercase_word}-{words[i+1].lower()}"
                if combined_word in [district.lower() for district in districts] or combined_word in [province.lower() for province in provinces]:
                    entities.append(combined_word.title())
                    i += 1
                    continue  # Skip to the next iteration
            entities.append(word.title())  # Append the original word
        if lemmatized_word in [weather_condition.lower() for weather_condition in weather_conditions]:
          entities.append(lemmatized_word)
        if lemmatized_word in [time.lower() for time in times]:
          entities.append(lemmatized_word)
        if re.match(r'\b\d+(\.\d+)?\b', word, re.IGNORECASE):
          entities.append(word + ' ' +words[i + 1])  # Append the time-like pattern

        i += 1

    return entities

def create_dictionary(entities):
    city_weather_mapping = {weather: {'cities': [], 'wind_speed': [], 'rainfall': [], 'time':[] } for weather in weather_conditions}
    current_weather = None  # Variable to keep track of the current weather condition
    for entity in entities:
        if entity in weather_conditions:  # If entity is a weather condition
            current_weather = entity  # Update current weather condition
            if current_weather not in city_weather_mapping:  # Ensure weather condition is not already in the mapping
                city_weather_mapping[current_weather] = []  # Initialize list for cities under current weather condition
        elif current_weather is not None:  # If entity is a city and a weather condition has been encountered
            if entity in districts or entity in provinces:
                city_weather_mapping[current_weather]['cities'].append(entity)
            elif entity in times:
                city_weather_mapping[current_weather]['time'].append(entity)
            elif 'kmph' in entity:
                city_weather_mapping[current_weather]['wind_speed'].append(entity)
            elif 'a.m' in entity or 'am' in entity or 'p.m' in entity or 'pm' in entity:
                city_weather_mapping[current_weather]['time'].append(entity)
            else:
                city_weather_mapping[current_weather]['rainfall'].append(entity)
    return city_weather_mapping

def print_weather_mapping_dictionary(city_weather_mapping):
    for weather, info in city_weather_mapping.items():
        if any(info[key] for key in ['cities', 'wind_speed', 'rainfall', 'time']):  # Check if any list contains data
            print(weather + ":")
            if info['cities']:
                print("  Cities:", info['cities'])
            if info['wind_speed']:
                print("  Wind Speed:", info['wind_speed'])
            if info['rainfall']:
                print("  Rainfall:", info['rainfall'])
            if info['time']:
                print("  Time:", info['time'])

# Function to fetch coordinates for a given city using OpenStreetMap Nominatim
def get_city_coordinates(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}, Sri Lanka&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return [lat, lon]
    return None

def display_map(dictionary):
    sri_lanka_data = gpd.read_file("srilanka.geojson") # Load Sri Lanka shapefile or GeoJSON data
    fig, ax = plt.subplots(figsize=(10, 10))
    sri_lanka_data.plot(ax=ax, color='white', edgecolor='black')
    #ax.set_title("Sri Lanka Map")
    plotted_cities = set() # Track cities that have already been plotted
    # Iterate over city_weather_mapping dictionary
    for weather_condition, weather_info in dictionary.items():
        cities = weather_info['cities']
        for idx, city in enumerate(cities):
            # Check if the city has already been plotted
            if city in plotted_cities:
                continue
            coordinates = get_city_coordinates(city)
            if coordinates:
                # Load and resize custom marker image based on weather condition
                image_path = icon_paths.get(weather_condition)
                if image_path:
                    custom_marker = Image.open(image_path)
                    custom_marker = custom_marker.resize((20, 20))  # Adjust the size as needed

                    # Adjust x-coordinate based on index to prevent overlapping
                    x_offset = (idx - len(cities) // 2) * 0.01 # Center the markers around the city
                    adjusted_lon = coordinates[1] + x_offset

                    # Add custom marker image at the adjusted coordinate
                    imagebox = OffsetImage(custom_marker)
                    ab = AnnotationBbox(imagebox, (adjusted_lon, coordinates[0]), frameon=False)
                    ax.add_artist(ab)

                    # Add text label at the specified coordinate
                    #ax.text(adjusted_lon, coordinates[0], city, fontsize=6, color='black', ha='center', va='top')
                    ax.text(adjusted_lon, coordinates[0], f"\n{city}", fontsize=8, color='black', ha='center', va='top', weight='bold')
                    
                    # Add the city to the set of plotted cities
                    plotted_cities.add(city)
    plt.axis('off')  # Turn off axis
    plt.show() # Show the plot

def sentence_split_from_paragraph(paragraph):
    sentences = paragraph.splitlines()
    return sentences

def main():
    sentences = sentence_split_from_paragraph(sentence3)
    for sentence in sentences:
        print(sentence.strip()) 
        entities = extract_all_entities(sentence, districts, provinces) # Extract locations from the sentence
        dictionary = create_dictionary(entities)
        print_weather_mapping_dictionary(dictionary)
        display_map(dictionary)

if __name__ == "__main__":
    main()

