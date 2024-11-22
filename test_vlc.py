# test_vlc.py

import vlc

try:
    instance = vlc.Instance()
    print("VLC Instance created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
