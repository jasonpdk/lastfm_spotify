import requests;
import spotipy
import spotipy.util as util

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

### LAST FM
## get top tracks for last 7 days

base_url = "http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&format=json"

user = "jasonpdk"
period = "7day"
api_key = "api_key"
page = 1
limit = 0

params = {
    "user": user,
    "api_key": api_key,
    "period": period
}

if (limit > 0):
    params['limit'] = limit

response = requests.get(url = base_url, params = params).json()

num_pages = int(response['toptracks']['@attr']['totalPages'])

tracks = []

for page in range(2, num_pages+1):
    tracks_response = response['toptracks']['track']

    track = 0
    for track in range(len(tracks_response)):
        tracks.append({
            "name": tracks_response[track]['name'],
            "artist": tracks_response[track]['artist']['name']
        })

    # if a limit is set 
    if (limit > 0 and track >= limit-1):
        break

    params['page'] = page
    response = requests.get(url = base_url, params = params).json()

### SPOTIFY AUTH ###
username = 'jasonpdk'
client_id = 'XYZ'
client_secret = 'XYZ'
redirect_uri = 'XYZ'
playlist_id = 'XYZ'

token = util.prompt_for_user_token(username, scope='playlist-modify-private,playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

sp_track_ids = []

# search for each track and add the IDs to a list
for track in range(len(tracks)):
    sp_query = tracks[track]['name'] + ' ' + tracks[track]['artist']
    results = sp.search(q=sp_query, type='track', limit=1)

    for i, t in enumerate(results['tracks']['items']):
        sp_track_ids.append(t['id'])

# Add the tracks to the playlist in batches of 100
if (len(sp_track_ids) > 100):
    track_ids_chunked = list(divide_chunks(sp_track_ids, 100))

    for i in range(len(track_ids_chunked)):
        if (i == 0):
            sp.user_playlist_replace_tracks(user=username, playlist_id=playlist_id, tracks=track_ids_chunked[i])
        else:
            sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_ids_chunked[i])
else:
    sp.user_playlist_replace_tracks(user=username, playlist_id=playlist_id, tracks=sp_track_ids)

