import time
import os
from get_generated_video import get_generated_video
from image_to_video import generate_video_id


current_directory = os.getcwd()

# Create the path to the "images" directory
images_directory = os.path.join(current_directory, "images")
files_in_folder = os.listdir(images_directory)
print(files_in_folder)




# weather_data = {
#     "shower": {
#         "Cities": ['Eastern', 'Uva', 'Polonnaruwa', 'Matale', 'Nuwara-Eliya', 'Northern', 'Anuradhapura', 'Western', 'Sabaragamuwa', 'Galle', 'Matara'],
#         "Time": ['2.00 p.m.']
#     },
#     "misty": {
#         "Cities": ['Western', 'Sabaragamuwa', 'Galle', 'Matara'],
#         "Time": ['morning']
#     },
#     "wind": {
#         "Cities": ['Eastern', 'Central', 'Northern', 'North-Central', 'Southern', 'North-Western', 'Uva', 'Eastern'],
#         "Wind Speed": ['30-40 kmph']
#     }
# }
#
#
# image_location = "./rainy_day.jpg"
#
# response  = generate_video_id(image_location)
#
# image_id =response.json()['id']
# print(image_id)
#
# response_status = 202
# while(response_status!=200):
#     response = get_generated_video("55f2d4353820fa5e83e2f193b8ef576a795e5cdeefed3c80289463c6d3438100")
#     response_status = response.status_code
#     if response.status_code == 202:
#         print("Generation in-progress, try again in 10 seconds.")
#         time.sleep(15)
#     elif response.status_code == 200:
#         print("Generation complete!")
#         with open("video_3.mp4", 'wb') as file:
#             file.write(response.content)
#     else:
#         raise Exception(str(response.json()))
#         break



























# import base64
# import os
# import requests
#
# engine_id = "stable-diffusion-v1-6"
# api_host = os.getenv('API_HOST', 'https://api.stability.ai')
# api_key = "sk-kxMvqmynYxEvqvkqvHwfUOJ5b96gtsNsYdrMcWcwscuSqRkH"
# # api_key = os.getenv("sk-kxMvqmynYxEvqvkqvHwfUOJ5b96gtsNsYdrMcWcwscuSqRkH")
#
# if api_key is None:
#     raise Exception("Missing Stability API key.")
#
# response = requests.post(
#     f"{api_host}/v1/generation/{engine_id}/text-to-image",
#     headers={
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     },
#     json={
#         "text_prompts": [
#             {
#                 "text": "Rainy evening near a lake"
#             }
#         ],
#         "cfg_scale": 7,
#         "height": 1024,
#         "width": 1024,
#         "samples": 1,
#         "steps": 30,
#     },
# )
#
# if response.status_code != 200:
#     raise Exception("Non-200 response: " + str(response.text))
#
# data = response.json()
# print(data["artifacts"])
#
# for i, image in enumerate(data["artifacts"]):
#     with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
#         f.write(base64.b64decode(image["base64"]))
