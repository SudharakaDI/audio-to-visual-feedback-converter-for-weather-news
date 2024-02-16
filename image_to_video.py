import requests

image_location = "./rainy_day.jpg"
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

