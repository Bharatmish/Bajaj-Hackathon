# app/documents/downloader.py
import os
import requests

def download_document(url: str, save_dir: str = "data/raw/") -> str:
    os.makedirs(save_dir, exist_ok=True)
    filename = url.split("?")[0].split("/")[-1]
    filepath = os.path.join(save_dir, filename)

    if not os.path.exists(filepath):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
        else:
            raise Exception(f"Failed to download file: {response.status_code}")
    return filepath
