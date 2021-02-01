import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


class Spotify(object):
    def __init__(self, access_token):
        self.prefix_url = "https://api.spotify.com/v1/"
        self.header = {"Authorization": f"Bearer {access_token['access_token']}"}
        self.access_token = access_token

    def set_access_token(self, access_token):
        self.header = {"Authorization": f"Bearer {access_token['access_token']}"}
        self.access_token = access_token

        URL = "https://accounts.spotify.com/api/token"
        refresh_token = self.access_token["refresh_token"]
        body_params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.post(URL, data=body_params).json()
        self.access_token = response
        self.access_token["refresh_token"] = refresh_token
        return self.access_token

    def _api_request(self, http_method, url, payload, params):
        headers = self.header
        headers["Content-Type"] = "application/json"
        if not url.startswith("http"):
            url = self.prefix_url + url
        if http_method == "GET":
            return requests.get(url, headers=headers, data=payload, params=params)
        if http_method == "POST":
            return requests.post(url, headers=headers, data=payload, params=params)
        return None

    def _get(self, url, payload=None, **kwargs):
        return self._api_request("GET", url, payload, kwargs)

    def _post(self, url, payload=None, **kwargs):
        return self._api_request("POST", url, payload, kwargs)

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
        elif id.startswith("http"):
            return id.split("/")[-1]
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
        track_id = self._get_id("track", id)
        return self._get(f"tracks/{track_id}")

    def get_current_user(self):
        return self._get("me")

    def get_user(self, id):
        user_id = self._get_id("user", id)
        return self._get(f"users/{user_id}")

    def get_playlist_items(self, id):
        playlist_id = self._get_id("playlist", id)
        return self._get(f"playlists/{playlist_id}/tracks")

    def get_current_user_playlists(self, limit=50, offset=0):
        return self._get(f"me/playlists", limit=limit, offset=offset)

    def get_top_tracks(self, limit=50, time_range="short_term"):
        return self._get("me/top/tracks", limit=limit, time_range=time_range)

    def create_playlist(
        self, user_id, name, public=True, collaborative=False, description=None
    ):
        return self._post(
            f"users/{user_id}/playlists",
            name=name,
            public=public,
            collaborative=collaborative,
            description=description,
        )

    def add_track_to_playlist(self, playlist_id, tracks):
        return self._post(f"playlists/{playlist_id}/tracks", uris=tracks)

    def get_uri_for_track(self, title, artist=None, album=None):
        return self._get(
            "search",
            q=f"track: {title} artist: {artist} album:{album}",
            type="track",
            limit=2,
        )