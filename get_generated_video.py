import requests

generation_id = "89b15aa4a2454c6f347e26ef835c0c4aef1510f568dbd970f568950ec149b77d"

def get_generated_video(generation_id):
    response = requests.request(
        "GET",
        f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
        headers={
            'Accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
            'authorization': f"Bearer sk-kxMvqmynYxEvqvkqvHwfUOJ5b96gtsNsYdrMcWcwscuSqRkH"
        },
    )

    return response

