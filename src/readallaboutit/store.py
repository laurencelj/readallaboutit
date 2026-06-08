import os
from supabase import create_client

def get_client():
    # These will look at the environment variables loaded by ingest.py
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_KEY"]
    )

def store_articles(articles):
    if not articles:
        return 0

    client = get_client()
    result = client.table("articles").upsert(
        articles,
        on_conflict="id"
    ).execute()

    return len(result.data)
