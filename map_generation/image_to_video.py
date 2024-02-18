import requests

# image_location = "./rainy_day.jpg"
def generate_video_id(image_location):
    response = requests.post(
        f"https://api.stability.ai/v2alpha/generation/image-to-video",
        headers={"authorization": f"Bearer sk-kxMvqmynYxEvqvkqvHwfUOJ5b96gtsNsYdrMcWcwscuSqRkH"},
        files={"image": open(image_location, "rb")},
        data={
            "seed": 0,
            "cfg_scale": 1.8,
            "motion_bucket_id": 127
        },
    )
    return response

def get_video_names(image_names,files_in_folder):
    video_names = []
    for image_name in image_names:
        if image_name in files_in_folder:
            video_names.append(image_name.split(".")[0])
        else:
            video_names.append(image_name.split("_")[0]+"_"+"common")

    video_names = list(set(video_names))
    print(video_names)
    return video_names
