import requests

generation_id = "64e3f488eac15402f37eae191f93dfd74b2959d22a10fdeca1893ec72658be55"

response = requests.request(
    "GET",
    f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
    headers={
        'Accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
        'authorization': f"Bearer sk-kxMvqmynYxEvqvkqvHwfUOJ5b96gtsNsYdrMcWcwscuSqRkH"
    },
)

if response.status_code == 202:
    print("Generation in-progress, try again in 10 seconds.")
elif response.status_code == 200:
    print("Generation complete!")
    with open("video.mp4", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))