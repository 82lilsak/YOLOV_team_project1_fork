import cv2
import handtrackingmodule as ht
import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time



def initialize_spotify():
    auth_manager = SpotifyOAuth(
        client_id='a76b120992a8421cb66efadf2108bea9',
        client_secret='abe9b41a94ab460095e869adcb269384',
        redirect_uri='http://localhost:8080/',
        scope='user-library-read user-library-modify user-read-playback-state user-modify-playback-state'
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']  # 첫 번째 장치 ID를 선택
        sp.start_playback(device_id=device_id)
    else:
        print("No active devices found.")

    return sp