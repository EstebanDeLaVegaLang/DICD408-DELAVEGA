import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configura tus credenciales
SPOTIPY_CLIENT_ID = 'tu_client_id'
SPOTIPY_CLIENT_SECRET = 'tu_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

scope = 'user-library-read user-top-read'

# Autenticación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Obtener información del usuario
results = sp.current_user_top_artists(limit=10)

for idx, artist in enumerate(results['items']):
    print(f"{idx + 1}: {artist['name']}")

# Buscar una canción
track_name = "Imagine"
results = sp.search(q=f"track:{track_name}", type='track', limit=1)

track = results['tracks']['items'][0]
print(f"Track: {track['name']}")
print(f"Artist: {track['artists'][0]['name']}")
print(f"URL: {track['external_urls']['spotify']}")
