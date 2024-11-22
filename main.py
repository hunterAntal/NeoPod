# main.py
import re
import feedfinder2
from database_manager import DatabaseManager
from feed_parser import FeedParser
from audio_manager import AudioManager
import threading
import time
import sys




def main_menu():
    print("\nNeoPod CLI")
    print("-----------")
    print("1. Subscribe to Podcast")
    print("2. View Subscriptions")
    print("3. Play Episode")
    print("4. Unsubscribe from Podcast")
    print("5. Play MP3 from URL")
    print("6. Exit")


def is_valid_url(url):
    url_pattern = re.compile(r'^https?://.+')
    return url_pattern.match(url) is not None

def subscribe_podcast():
    url = input("Enter RSS Feed URL or Website URL: ").strip()
    print(f"DEBUG: URL entered = {url}")
    if not is_valid_url(url):
        print("Invalid URL format. Please enter a valid URL starting with http:// or https://")
        return

    parser = FeedParser()

    # Try parsing the URL as an RSS feed
    podcast_info = parser.parse_feed(url)
    if podcast_info['title'] == 'No Title' and not podcast_info['episodes']:
        # Not a valid feed, try finding feeds with Feedfinder
        print("The URL provided is not a valid RSS feed. Attempting to find feeds on the website...")
        try:
            feeds = feedfinder2.find_feeds(url)
        except Exception as e:
            print(f"An error occurred while searching for feeds: {e}")
            return

        if not feeds:
            print("No RSS feeds found at the provided URL.")
            return
        elif len(feeds) == 1:
            feed_url = feeds[0]
            print(f"Found feed: {feed_url}")
        else:
            print("Multiple feeds found:")
            for idx, feed in enumerate(feeds, 1):
                print(f"{idx}. {feed}")
            while True:
                choice = input("Select a feed to subscribe to (Enter the number): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(feeds):
                    feed_url = feeds[int(choice) - 1]
                    break
                else:
                    print("Invalid choice. Please try again.")
        # Try parsing the selected feed
        podcast_info = parser.parse_feed(feed_url)
        if podcast_info['title'] == 'No Title' and not podcast_info['episodes']:
            print("Failed to parse the selected feed.")
            return
    else:
        feed_url = url  # The original URL is a valid feed

    db_manager = DatabaseManager()
    db_manager.add_podcast(podcast_info['title'], feed_url, podcast_info['description'])
    db_manager.close()

    print(f"Subscribed to {podcast_info['title']}")



def view_subscriptions():
    db_manager = DatabaseManager()
    subscriptions = db_manager.get_subscriptions()
    db_manager.close()

    if subscriptions:
        print("Your Subscriptions:")
        for idx, (podcast_id, title) in enumerate(subscriptions, 1):
            print(f"{idx}. {title}")
    else:
        print("You have no subscriptions.")

def play_episode():
    db_manager = DatabaseManager()
    while True:
        subscriptions = db_manager.get_subscriptions()

        if not subscriptions:
            print("You have no subscriptions.")
            db_manager.close()
            return

        print("\nSelect a Podcast (Enter 0 to return to main menu):")
        for idx, (podcast_id, title) in enumerate(subscriptions, 1):
            print(f"{idx}. {title}")

        choice_input = input("Enter choice number: ").strip()
        if choice_input == '0':
            db_manager.close()
            return  # Return to main menu
        if not choice_input.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        choice = int(choice_input) - 1
        if choice < 0 or choice >= len(subscriptions):
            print("Invalid choice. Please try again.")
            continue
        selected_podcast = subscriptions[choice]
        podcast_id, podcast_title = selected_podcast

        # Fetch episodes
        cursor = db_manager.conn.cursor()
        cursor.execute('SELECT feed_url FROM podcasts WHERE id = ?', (podcast_id,))
        feed_url = cursor.fetchone()[0]

        parser = FeedParser()
        podcast_info = parser.parse_feed(feed_url)
        episodes = podcast_info['episodes']
        episodes.reverse()  # Show latest episodes first

        while True:
            print(f"\nEpisodes for {podcast_title} (Enter 0 to go back):")
            for idx, episode in enumerate(episodes, 1):
                print(f"{idx}. {episode['title']}")

            episode_choice_input = input("Select an episode to play: ").strip()
            if episode_choice_input == '0':
                break  # Go back to podcast selection
            if not episode_choice_input.isdigit():
                print("Invalid choice. Please enter a number.")
                continue
            episode_choice = int(episode_choice_input) - 1
            if episode_choice < 0 or episode_choice >= len(episodes):
                print("Invalid choice. Please try again.")
                continue
            selected_episode = episodes[episode_choice]

            audio_manager = AudioManager()
            print(f"\nNow playing: {selected_episode['title']}")
            audio_manager.play_episode(selected_episode['url'])

            # Start a thread to listen for user input during playback
            input_thread = threading.Thread(target=playback_controls, args=(audio_manager,))
            input_thread.daemon = True  # Daemonize thread
            input_thread.start()

            # Wait for playback to finish
            while audio_manager.is_playing():
                time.sleep(1)  # Sleep briefly to reduce CPU usage

            print("\nPlayback finished.")

            # Ask if the user wants to play another episode
            while True:
                continue_choice = input("\nDo you want to play another episode? (y/n): ").strip().lower()
                if continue_choice == 'y':
                    break  # Stay in the episode selection loop
                elif continue_choice == 'n':
                    break  # Exit to podcast selection
                else:
                    print("Please enter 'y' or 'n'.")
            if continue_choice == 'y':
                continue  # Continue in the episode selection loop
            else:
                break  # Exit to podcast selection
    db_manager.close()

def playback_controls(audio_manager):
    print("\nPress '1' to Pause, '2' to Play, '0' to Stop and return to the episode list.")
    while audio_manager.is_playing():
        user_input = input()
        if user_input == '1':
            audio_manager.pause()
            print("Paused.")
        elif user_input == '2':
            audio_manager.resume()
            print("Resumed.")
        elif user_input == '0':
            audio_manager.stop()
            print("Stopped playback.")
            break
        else:
            print("Invalid input. Press '1' to Pause, '2' to Play, '0' to Stop.")

def unsubscribe_podcast():
    db_manager = DatabaseManager()
    subscriptions = db_manager.get_subscriptions()

    if not subscriptions:
        print("You have no subscriptions.")
        db_manager.close()
        return

    print("\nSelect a Podcast to Unsubscribe (Enter 0 to return to main menu):")
    for idx, (podcast_id, title) in enumerate(subscriptions, 1):
        print(f"{idx}. {title}")

    while True:
        choice_input = input("Enter choice number: ").strip()
        if choice_input == '0':
            db_manager.close()
            return  # Return to main menu
        if not choice_input.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        choice = int(choice_input) - 1
        if choice < 0 or choice >= len(subscriptions):
            print("Invalid choice. Please try again.")
            continue
        selected_podcast = subscriptions[choice]
        podcast_id, podcast_title = selected_podcast

        # Confirm unsubscription
        confirm = input(f"Are you sure you want to unsubscribe from '{podcast_title}'? (y/n): ").strip().lower()
        if confirm == 'y':
            db_manager.remove_podcast(podcast_id)
            print(f"Unsubscribed from '{podcast_title}'.")
        else:
            print("Unsubscription cancelled.")

        db_manager.close()
        break

def play_mp3_from_url():
    url = input("Enter MP3 URL: ").strip()
    if not url:
        print("No URL entered.")
        return

    audio_manager = AudioManager()
    print(f"\nAttempting to play: {url}")

    try:
        # Play the MP3 URL
        audio_manager.play_episode(url)

        # Start a thread to listen for user input during playback
        input_thread = threading.Thread(target=playback_controls, args=(audio_manager,))
        input_thread.daemon = True  # Daemonize thread
        input_thread.start()

        # Wait for playback to finish
        while audio_manager.is_playing():
            time.sleep(1)  # Sleep briefly to reduce CPU usage

        print("\nPlayback finished.")

    except Exception as e:
        print(f"An error occurred while playing the MP3: {e}")

def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            subscribe_podcast()
        elif choice == '2':
            view_subscriptions()
        elif choice == '3':
            play_episode()
        elif choice == '4':
            unsubscribe_podcast()
        elif choice == '5':
            play_mp3_from_url()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
