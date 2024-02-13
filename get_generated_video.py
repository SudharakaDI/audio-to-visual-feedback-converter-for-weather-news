import requests

generation_id = "89b15aa4a2454c6f347e26ef835c0c4aef1510f568dbd970f568950ec149b77d"

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