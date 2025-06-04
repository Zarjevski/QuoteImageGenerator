import requests
import os

ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
PAGE_ID = os.getenv("IG_PAGE_ID")
IG_USER_ID = os.getenv("IG_USER_ID")

def post_to_instagram(image_path, caption):
    # 1. Upload image to container
    url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
    files = {"image_url": ("image", open(image_path, "rb"))}
    data = {
        "caption": caption,
        "access_token": ACCESS_TOKEN,
    }

    res = requests.post(url, data=data)
    container_id = res.json().get("id")

    # 2. Publish container
    pub_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"
    publish = requests.post(pub_url, data={
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    })

    return publish.status_code == 200
