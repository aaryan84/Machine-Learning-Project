from flask import Flask, render_template, request
import pandas as pd
from spotify_auth import get_spotify_client
import joblib

app = Flask(__name__)

# Authenticate with Spotify
sp = get_spotify_client()

# Load K-Means model and clustered data
kmeans = joblib.load('kmeans_model.pkl')
df = pd.read_csv('song_clusters.csv')

# Mapping moods to clusters
mood_to_cluster_map = {
    'happy': 0,
    'sad': 1,
    'energetic': 2,
    'relaxed': 3,
    'neutral': 4
}

@app.route('/')
def index():
    return render_template('index.html', recommendations=[])

@app.route('/recommend', methods=['POST'])
def recommend():
    mood = request.form['mood'].lower()

    # Get cluster based on mood
    cluster = mood_to_cluster_map.get(mood, 4)  # Default to 'neutral'
    recommended_songs = df[df['cluster'] == cluster].sample(5)

    # Fetch song details from Spotify
    recommendations = []
    for song_id in recommended_songs['id']:
        track = sp.track(song_id)
        recommendations.append({
            'name': track['name'],
            'artist': ", ".join(artist['name'] for artist in track['artists']),
            'link': track['external_urls']['spotify']
        })

    return render_template('index.html', recommendations=recommendations)

@app.route('/reset', methods=['POST'])
def reset():
    return render_template('index.html', recommendations=[])

if __name__ == '__main__':
    app.run(debug=True)
