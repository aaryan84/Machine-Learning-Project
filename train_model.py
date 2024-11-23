import pandas as pd
from sklearn.cluster import KMeans
import joblib
from spotify_auth import get_spotify_client

# Authenticate with Spotify
sp = get_spotify_client()

# Fetch data
tracks = sp.search(q="mood", type='track', limit=50)
features = sp.audio_features([track['id'] for track in tracks['tracks']['items']])

# Prepare data for clustering
df = pd.DataFrame(features)
df = df[['id', 'danceability', 'energy', 'valence']]  # Keep relevant features

# Train K-Means model
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(df[['danceability', 'energy', 'valence']])
df['cluster'] = kmeans.labels_

# Save the model and clustered data
joblib.dump(kmeans, 'kmeans_model.pkl')
df.to_csv('song_clusters.csv', index=False)
