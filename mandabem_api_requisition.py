import requests


payload = {
    "plataforma_id": "66780",
    "plataforma_chave": "$2y$10$1uqdW6t3fFS.4nk7nueRDujOYSPvTf81RSF88NADpFQXTjmT5C.HS"
}

url = "https://mandabem.com.br/ws/valor_envio"


response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
