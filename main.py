# main.py

from database_manager import DatabaseManager
from feed_parser import FeedParser
from audio_manager import AudioManager

def main_menu():
    print("NeoPod CLI")
    print("-----------")
    print("1. Subscribe to Podcast")
    print("2. View Subscriptions")
    print("3. Play Episode")
    print("4. Exit")

def subscribe_podcast():
    feed_url = input("Enter RSS Feed URL: ")
    parser = FeedParser()
    podcast_info = parser.parse_feed(feed_url)

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
    subscriptions = db_manager.get_subscriptions()

    if not subscriptions:
        print("You have no subscriptions.")
        db_manager.close()
        return

    print("Select a Podcast:")
    for idx, (podcast_id, title) in enumerate(subscriptions, 1):
        print(f"{idx}. {title}")

    choice = int(input("Enter choice number: ")) - 1
    selected_podcast = subscriptions[choice]
    podcast_id, podcast_title = selected_podcast

    # Fetch episodes
    cursor = db_manager.conn.cursor()
    cursor.execute('SELECT feed_url FROM podcasts WHERE id = ?', (podcast_id,))
    feed_url = cursor.fetchone()[0]

    parser = FeedParser()
    podcast_info = parser.parse_feed(feed_url)
    episodes = podcast_info['episodes']

    print(f"Episodes for {podcast_title}:")
    for idx, episode in enumerate(episodes, 1):
        print(f"{idx}. {episode['title']}")

    episode_choice = int(input("Select an episode to play: ")) - 1
    selected_episode = episodes[episode_choice]

    audio_manager = AudioManager()
    print(f"Now playing: {selected_episode['title']}")
    audio_manager.play_episode(selected_episode['url'])

    input("Press Enter to stop playback...")
    audio_manager.stop()
    db_manager.close()

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
