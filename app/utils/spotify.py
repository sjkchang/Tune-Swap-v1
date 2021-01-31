import requests
import json


class Spotify(object):
    def __init__(self, access_token):
        self.prefix_url = "https://api.spotify.com/v1/"
        self.header = {"Authorization": f"Bearer {access_token}"}
        self.access_token = access_token

    def _api_request(self, http_method, url, payload, params):
        headers = self.header
        headers["Content-Type"] = "application/json"
        if not url.startswith("http"):
            url = self.prefix_url + url
        if http_method == "GET":
            return requests.get(url, headers=headers, data=payload, params=params)
        return None

    def _get(self, url, payload=None, **kwargs):
        return self._api_request("GET", url, payload, kwargs)

    def _get_id(self, type, id):
        """Returns the id of a spotify api object given a id, uri or url

        Args:
            type ([String]): The type of the spotify object whose id we are fetching
            id ([String]): The id, uri or url of the spotify api object

        Returns:
            [String]: The id of the spotify api object
        """

        # If the given id is a uri, return the id which is the last section of the uri
        if self._is_uri(id):
            return id.split(":")[2]
        # Otherwise if it is a url return the content following the last /
        # elif self.is_url():
        # return id.split("/")[-1]
        # If the passed id is not a url or a uri, it is a id, so just return it
        return id

    def _get_uri(self, type, id):
        """Returns the uri of a spotify api object, given a id, uri, or url

        Args:
            type (String): The type of the spotify api object whose uri we are fetching
            id (String): The id, uri, or url of the spotify api object

        Returns:
            [String]: The uri of the spotify api object
        """
        if self.is_uri(id):
            return f"spotify:{type}:{id}"
        else:
            return f"spotify:{type}:{self._get_id(type, id)}"

    def _is_uri(self, uri):
        """Returns True if the uri parameter is a uri. A valid uri is a string with three parts
        the word spotify, the type of the object, and the id, all seperated with :

        Args:
            uri (String): The String we are determining to be a uri or not

        Returns:
            [Boolean]: True if the param uri is a uri,
            False if the param uri is not a uri
        """
        return uri.startswith("spotify:") and len(uri.split(":")) == 3

    def get_track(self, id):
        """returns a track given the tracks id, uri, or url

        Args:
            id: a tracks id, uri or url
        """
        track_id = self._get_id("track", id)
        return self._get(f"tracks/{id}")

    def get_current_user(self):
        return self._get("me")

    def get_user(self, id):
        user_id = self._get_id("user", id)
        return self._get(f"users/{id}")


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
