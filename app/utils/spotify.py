import requests
import json


def getCurrentUserId(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers)
    response = response.json()
    id = response["id"]
    return id


def getCurrentUser(access_token):
    url = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers)
    response = response.json()

    return response


def get_playlists(access_token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": "Bearer " + access_token,
    }

    response = requests.get(url, headers=headers)
    response = response.json()

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
    params = {"fields": "name,description,uri"}

    response = requests.get(url, headers=headers)
    response = response.json()

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

    response = requests.get(url, headers=headers, params=params)
    response = response.json()

    return response


def create_playlist(access_token, name, description="", is_public=True):
    user_id = getCurrentUserId(access_token)
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    body_params = {"name": name, "public": is_public, "description": description}

    response = requests.post(url, data=json.dumps(body_params), headers=headers)
    print(response.text)
    response = response.json()

    return response


def add_track_to_playlist(access_token, playlist_id, track_uri):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }

    params = {"uris": [track_uri]}

    response = requests.post(url, headers=headers, data=json.dumps(params))
    response = response.json()
    return response