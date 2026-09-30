import pandas as pd
import feedparser
import random
from datetime import datetime
from utils.sentiment import analyze_sentiment_vader, analyze_sentiment_llm

def fetch_rss_data(rss_url: str, engine: str = "vader", api_key: str = None) -> pd.DataFrame:
    """Estrae notizie reali da un feed RSS e analizza il sentiment."""
    feed = feedparser.parse(rss_url)
    data = []
    
    for entry in feed.entries[:20]:
        title = entry.get('title', '')
        published = entry.get('published', str(datetime.now()))
        
        if engine == "vader":
            s_res = analyze_sentiment_vader(title)
        else:
            s_res = analyze_sentiment_llm(title, provider=engine, api_key=api_key)
            
        data.append({
            'timestamp': pd.to_datetime(published, errors='coerce') or datetime.now(),
            'post': title,
            'likes': random.randint(10, 500),
            'shares': random.randint(1, 100),
            'sentiment_category': s_res['category'],
            'sentiment_score': s_res.get('compound', 0.0)
        })
        
    df = pd.DataFrame(data)
    return df.sort_values(by='timestamp', ascending=False)