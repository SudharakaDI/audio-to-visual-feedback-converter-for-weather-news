import requests

generation_id = "64e3f488eac15402f37eae191f93dfd74b2959d22a10fdeca1893ec72658be55"

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

