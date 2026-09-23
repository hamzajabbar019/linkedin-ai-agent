import feedparser
from datetime import datetime


RSS_FEEDS = {
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
}


def get_latest_topics(limit_per_source=5):
    topics = []

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:limit_per_source]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                published = entry.get("published", "")

                if title:
                    topics.append({
                        "source": source,
                        "title": title,
                        "link": link,
                        "published": published
                    })

        except Exception as e:
            print(f"Could not read {source}: {e}")

    return topics


if __name__ == "__main__":
    topics = get_latest_topics()

    print("\n" + "=" * 60)
    print("LATEST AI TOPICS")
    print("=" * 60)

    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. {topic['title']}")
        print(f"   Source: {topic['source']}")
        print(f"   Link: {topic['link']}")

    print("\n" + "=" * 60)
    print(f"Total topics found: {len(topics)}")
    print("=" * 60)
