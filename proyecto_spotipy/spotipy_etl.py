import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Configuración de las credenciales
client_id = 'ad90ba5206b34e428a7a24bf467e854b'
client_secret = '2211383cb62f445bb2678128a15cb3db'
redirect_uri = 'http://localhost:8888/callback'  # La URI de redireccionamiento configurada en la app de Spotify
scope = 'user-library-read playlist-read-private user-follow-read'

# Autenticación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Funciones para extraer datos
def obtener_datos_usuarios(sp):
    user_profile = sp.current_user()
    datos_usuario = {
        'id': user_profile['id'],
        'nombre': user_profile['display_name'],
        'email': user_profile['email'],
        'pais': user_profile['country'],
        'seguidores': user_profile['followers']['total']
    }
    return pd.DataFrame([datos_usuario])

def obtener_datos_playlists(sp):
    playlists = sp.current_user_playlists()['items']
    datos_playlists = []
    for playlist in playlists:
        datos_playlists.append({
            'id': playlist['id'],
            'nombre': playlist['name'],
            'propietario': playlist['owner']['id'],
            'numero_canciones': playlist['tracks']['total'],
            'publica': playlist['public']
        })
    return pd.DataFrame(datos_playlists)

def obtener_datos_tracks(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    datos_tracks = []
    for item in tracks:
        track = item['track']
        datos_tracks.append({
            'id': track['id'],
            'nombre': track['name'],
            'album_id': track['album']['id'],
            'artista_id': track['artists'][0]['id'],
            'duracion_ms': track['duration_ms'],
            'popularidad': track['popularity']
        })
    return pd.DataFrame(datos_tracks)

def obtener_datos_albumes(sp, album_id):
    album = sp.album(album_id)
    datos_album = {
        'id': album['id'],
        'nombre': album['name'],
        'artista_id': album['artists'][0]['id'],
        'fecha_lanzamiento': album['release_date'],
        'total_pistas': album['total_tracks']
    }
    return pd.DataFrame([datos_album])

def obtener_datos_artistas(sp, artista_id):
    artista = sp.artist(artista_id)
    datos_artista = {
        'id': artista['id'],
        'nombre': artista['name'],
        'popularidad': artista['popularity'],
        'generos': ', '.join(artista['genres']),
        'seguidores': artista['followers']['total']
    }
    return pd.DataFrame([datos_artista])

# Ejecución de las funciones y guardado en CSV
datos_usuario_df = obtener_datos_usuarios(sp)
datos_usuario_df.to_csv('datos_usuario.csv', index=False)

datos_playlists_df = obtener_datos_playlists(sp)
datos_playlists_df.to_csv('datos_playlists.csv', index=False)

# Obtener datos de tracks, álbumes y artistas para cada playlist
datos_tracks_df = pd.DataFrame()
datos_albumes_df = pd.DataFrame()
datos_artistas_df = pd.DataFrame()

for playlist_id in datos_playlists_df['id']:
    tracks_df = obtener_datos_tracks(sp, playlist_id)
    datos_tracks_df = pd.concat([datos_tracks_df, tracks_df], ignore_index=True)
    for album_id in tracks_df['album_id'].unique():
        album_df = obtener_datos_albumes(sp, album_id)
        datos_albumes_df = pd.concat([datos_albumes_df, album_df], ignore_index=True)
    for artista_id in tracks_df['artista_id'].unique():
        artista_df = obtener_datos_artistas(sp, artista_id)
        datos_artistas_df = pd.concat([datos_artistas_df, artista_df], ignore_index=True)

datos_tracks_df.to_csv('datos_tracks.csv', index=False)
datos_albumes_df.to_csv('datos_albumes.csv', index=False)
datos_artistas_df.to_csv('datos_artistas.csv', index=False)
