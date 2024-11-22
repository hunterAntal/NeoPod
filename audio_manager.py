# audio_manager.py

import vlc

class AudioManager:
    def __init__(self):
        try:
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
        except Exception as e:
            print(f"An error occurred while initializing VLC: {e}")
            raise

    def play_episode(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.is_playing()

    def get_position(self):
        return self.player.get_time()  # In milliseconds

    def set_position(self, time_ms):
        self.player.set_time(time_ms)
