import requests
import json

url = "http://127.0.0.1:8000/api/v1/hackrx/run"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer e6722c98521d93e48a741430431ac4a42b2de812838206df9cc46a4fe6795b5b"
}

data = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
    ]
}

response = requests.post(url, headers=headers, json=data)

# Print debug info
print("Status Code:", response.status_code)
print("Raw Response Text:")
print(response.text)
