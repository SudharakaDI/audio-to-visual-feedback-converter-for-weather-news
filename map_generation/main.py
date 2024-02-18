
import os

from get_image_from_weather_data import get_images
from generate_videos import generate_videos
from image_to_video import generate_video_id, get_video_names

def get_available_image_file_names():
    current_directory = os.getcwd()

    # Create the path to the "images" directory
    images_directory = os.path.join(current_directory, "images")
    files_in_folder = os.listdir(images_directory)
    print(files_in_folder)

    return files_in_folder


weather_data = {
    "shower": {
        "Cities": ['Eastern', 'Uva', 'Polonnaruwa', 'Matale', 'Nuwara-Eliya', 'Northern', 'Anuradhapura', 'Western', 'Sabaragamuwa', 'Galle', 'Matara'],
        "Time": ['2.00 p.m.']
    },
    "misty": {
        "Cities": ['Western', 'Sabaragamuwa', 'Galle', 'Matara'],
        "Time": ['morning']
    },
    "wind": {
        "Cities": ['Eastern', 'Central', 'Northern', 'North-Central', 'Southern', 'North-Western', 'Uva', 'Eastern'],
        "Wind Speed": ['30-40 kmph']
    }
}
def run_video_generation_process(weather_data):
    image_names = get_images(weather_data)
    files_in_folder = get_available_image_file_names()
    video_names = get_video_names(image_names,files_in_folder)
    generate_videos(video_names)

# run_video_generation_process(weather_data)