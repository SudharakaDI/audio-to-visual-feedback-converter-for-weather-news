import requests

response = requests.post(
    f"https://api.stability.ai/v2alpha/generation/image-to-video",
    headers={"authorization": f"Bearer sk-kxMvqmynYxEvqvkqvHwfUOJ5b96gtsNsYdrMcWcwscuSqRkH"},
    files={"image": open("./rainy_day.jpg", "rb")},
    data={
        "seed": 0,
        "cfg_scale": 1.8,
        "motion_bucket_id": 127
    },
)

print(response.json())