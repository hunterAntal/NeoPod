# main.py

from database_manager import DatabaseManager
from feed_parser import FeedParser
from audio_manager import AudioManager

def main_menu():
    print("\nNeoPod CLI")
    print("-----------")
    print("1. Subscribe to Podcast")
    print("2. View Subscriptions")
    print("3. Play Episode")
    print("4. Exit")

def subscribe_podcast():
    feed_url = input("Enter RSS Feed URL: ").strip()
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

            episode_choice_input = input("Select an episode to play (Enter 0 to return to main menu): ").strip()
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

            input("Press Enter to stop playback...")
            audio_manager.stop()

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
