import requests

def check_virustotal(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": "your_api_key"}
    response = requests.get(url, headers=headers)
    return response.json()