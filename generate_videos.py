from image_to_video import generate_video_id
from get_generated_video import get_generated_video
import time

def generate_videos(video_names):
    for video_name in video_names:
        image_location = "./images/" + video_name + ".jpg"
        response = generate_video_id(image_location)
        image_id = response.json()['id']
        print(image_id)

        response_status = 202
        while (response_status != 200):
            response = get_generated_video(image_id)
            response_status = response.status_code
            if response.status_code == 202:
                print("Generation in-progress, try again in 10 seconds.")
                time.sleep(15)
            elif response.status_code == 200:
                print("Generation complete!")
                with open("./generated_video/" + video_name + ".mp4", 'wb') as file:
                    file.write(response.content)
            else:
                raise Exception(str(response.json()))
                break
