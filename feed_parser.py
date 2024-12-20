import feedparser

class FeedParser:
    def parse_feed(self, url):
        feed = feedparser.parse(url)

        if feed.bozo:
            # An error occurred while parsing the feed
            print(f"Error parsing feed: {feed.bozo_exception}")
            return {'title': 'No Title', 'description': 'No Description', 'episodes': []}

        podcast_info = {
            'title': feed.feed.get('title', 'No Title'),
            'description': feed.feed.get('description', 'No Description'),
            'episodes': []
        }

        for entry in feed.entries:
            episode = {
                'title': entry.get('title', 'No Title'),
                'url': entry.enclosures[0].href if entry.enclosures else None,
                'pub_date': entry.get('published', 'No Publication Date'),
                'duration': entry.get('itunes_duration', 'Unknown Duration')
            }
            podcast_info['episodes'].append(episode)

        return podcast_info
