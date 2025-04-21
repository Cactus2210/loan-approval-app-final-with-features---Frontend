import requests

def call_api(endpoint: str, data: dict):
    base_url = "https://web-production-8a84a.up.railway.app/"
    try:
        print("🚀 Sending to API:", data)
        res = requests.post(f"{base_url}{endpoint}", json=data)
        print("🛬 Response:", res.status_code, res.text)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
