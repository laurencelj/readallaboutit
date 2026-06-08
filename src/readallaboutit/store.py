from supabase import create_client
import os

def get_client():
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_KEY"]
    )

def store_articles(articles):
    client = get_client()
    result = client.table("articles").upsert(
        articles,
        on_conflict="id"
    ).execute()
    return len(result.data)
