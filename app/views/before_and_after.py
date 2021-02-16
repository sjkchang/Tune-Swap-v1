from flask import current_app as app
from flask import redirect, request, url_for, session, g

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from ..utils.spotify import Spotify

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
BASE_URL = "https://accounts.spotify.com/authorize"
