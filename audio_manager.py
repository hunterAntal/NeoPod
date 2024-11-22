# audio_manager.py

import vlc
import threading
import time  


class AudioManager:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.lock = threading.Lock()  # To synchronize access to the player

    def play_episode(self, url, retries=3):
            for attempt in range(retries):
                media = self.instance.media_new(url)
                self.player.set_media(media)
                try:
                    self.player.play()
                    if self.wait_for_playback_start():
                        return
                    else:
                        print(f"Attempt {attempt + 1} failed to start playback.")
                except Exception as e:
                    print(f"An error occurred during playback: {e}")
                    self.stop()
                # Wait before retrying
                time.sleep(5)
            print("Failed to start playback after multiple attempts.")


    def pause(self):
        with self.lock:
            if self.player.is_playing():
                self.player.pause()

    def resume(self):
        with self.lock:
            self.player.play()

    def stop(self):
        with self.lock:
            self.player.stop()

    def is_playing(self):
        return self.player.is_playing()
    
    def wait_for_playback_start(self, timeout=30):
        import time
        start_time = time.time()
        print(f"Waiting for playback to start (timeout in {timeout} seconds)...")
        while time.time() - start_time < timeout:
            state = self.player.get_state()
            if state == vlc.State.Playing:
                print("Playback started.")
                return True
            elif state in (vlc.State.Error, vlc.State.Ended):
                print("Playback encountered an error.")
                return False
            time.sleep(0.1)
        print("Playback did not start within the timeout period.")
        return False
    
    class AudioManager:
        def __init__(self):
            # Increase network caching to 5000 ms (5 seconds)
            self.instance = vlc.Instance('--network-caching=5000')
            self.player = self.instance.media_player_new()
            self.lock = threading.Lock()