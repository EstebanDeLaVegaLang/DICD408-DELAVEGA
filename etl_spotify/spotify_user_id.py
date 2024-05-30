import requests
import base64

# Reemplaza estos valores con los obtenidos al registrar tu aplicación en Spotify
client_id = 'ad90ba5206b34e428a7a24bf467e854b'
client_secret = '2211383cb62f445bb2678128a15cb3db'
redirect_uri = 'http://localhost:8888/callback'  # Debe coincidir con el registrado en Spotify

# Paso 1: Obtén el código de autorización
auth_url = "https://accounts.spotify.com/authorize"
params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": "user-read-private user-read-email"
}
response = requests.get(auth_url, params=params)
print("Ve a la siguiente URL y autoriza la aplicación:", response.url)

# Paso 2: Una vez autorizado, Spotify redirigirá a tu URI con un código de autorización en la URL
authorization_code = input("Introduce el código de autorización obtenido de la URL redirigida: ")

# Paso 3: Usa el código de autorización para obtener un token de acceso
token_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
}
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri
}
response = requests.post(token_url, headers=headers, data=data)
response_data = response.json()
access_token = response_data.get("access_token")

# Paso 4: Usa el token de acceso para obtener información del usuario
me_url = "https://api.spotify.com/v1/me"
headers = {
    "Authorization": f"Bearer {access_token}"
}
response = requests.get(me_url, headers=headers)
user_data = response.json()
user_id = user_data["id"]

print(f"Tu user_id es: {user_id}")
