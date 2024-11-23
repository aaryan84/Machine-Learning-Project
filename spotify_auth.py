import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    client_id = '5a5ac88b2a8c4612bb556df69a150a80'
    client_secret = 'f5679d1f37b442e69a6de5a37e4531b9'
    redirect_uri = 'http://localhost:5000/callback'

    scope = "user-library-read playlist-read-private user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    ))

    return sp
