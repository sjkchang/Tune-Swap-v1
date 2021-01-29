import requests
import json


def get_current_user_simplified(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers).json()
    id = response["id"]
    return id


def get_current_user(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers).json()

    return response


def get_playlists(access_token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers).json()

    return response


def get_playlists_simplified(access_token):
    response = get_playlists(access_token)
    items = response["items"]
    playlists = []
    for item in items:
        playlist = {
            "id": item["id"],
            "name": item["name"],
            "description": "Description",
            "uri": item["uri"],
            "public": item["public"],
            "platform": "Spotify",
        }
        playlists.append(playlist)
    return playlists


def get_playlist(access_token, playlist_id):
    print(playlist_id)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers).json()

    return response


def get_uri_for_track(access_token, title, artist, album):
    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": "Bearer " + access_token,
    }
    params = {
        "q": f"track: {title} artist: {artist} album:{album}",
        "type": "track",
        "limit": 2,
    }

    response = requests.get(url, headers=headers, params=params).json()

    return response


def create_playlist(access_token, name, description="", is_public=True):
    user_id = get_current_user_simplified(access_token)
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    body_params = {"name": name, "public": is_public, "description": description}

    response = requests.post(url, data=json.dumps(body_params), headers=headers).json()

    return response


def add_track_to_playlist(access_token, playlist_id, track_uri):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    params = {"uris": [track_uri]}

    response = requests.post(url, headers=headers, data=json.dumps(params)).json()
    return response


def get_top_tracks(access_token, time_range):
    url = "https://api.spotify.com/v1/me/top/tracks"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    params = {
        "time_range": time_range,
        "limit": 50,
    }

    response = requests.get(url, headers=headers, params=params).json()

    return response


def get_top_tracks_simplified(access_token, time_range):
    response = get_top_tracks(access_token, time_range)
    tracks = []
    for item in response["items"]:
        tracks.append(item)

    return tracks