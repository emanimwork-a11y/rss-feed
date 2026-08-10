import os
from ntscraper import Nitter
from feedgen.feed import FeedGenerator

# 1. Initialize Nitter Scraper (Log level 0 suppresses verbose logs)
scraper = Nitter(log_level=0)

# Target Twitter handle (without the @ symbol)
TWITTER_USER = "NASA" 

# 2. Fetch public tweets
print(f"Scraping tweets for @{TWITTER_USER}...")
try:
    # Fetch latest 15 tweets
    tweets_data = scraper.get_tweets(TWITTER_USER, mode='user', number=15)
    tweets = tweets_data.get('tweets', [])
except Exception as e:
    print(f"Error scraping tweets: {e}")
    tweets = []

# 3. Build the RSS feed structure
fg = FeedGenerator()
fg.title(f"X / Twitter Feed - @{TWITTER_USER}")
fg.link(href=f"https://x.com/{TWITTER_USER}", rel="alternate")
fg.description(f"Automated RSS feed for @{TWITTER_USER} posts")

# 4. Populate RSS items
for tweet in tweets:
    fe = fg.add_entry()
    # Use the first 60 characters of the tweet as title
    tweet_text = tweet.get('text', '')
    title_snippet = (tweet_text[:60] + '...') if len(tweet_text) > 60 else tweet_text
    
    fe.title(title_snippet if title_snippet else "New Post")
    fe.description(tweet_text)
    fe.link(href=tweet.get('link', f"https://x.com/{TWITTER_USER}"))
    
    # Optional: Attach publication date if available
    if tweet.get('date'):
        fe.published(tweet.get('date'))

# 5. Export feed XML file
fg.rss_file("twitter_feed.xml")
print("Feed successfully written to twitter_feed.xml")
