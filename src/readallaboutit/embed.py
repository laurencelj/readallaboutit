import os
import time
from openai import OpenAI
from supabase import create_client

def main():
    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_KEY"]
    )
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    # Fetch unembedded articles
    rows = supabase.table("articles")\
        .select("id, title, summary")\
        .is_("embedding", None)\
        .execute().data

    if not rows:
        print("No new articles to embed.")
        return

    print(f"Embedding {len(rows)} articles...")

    for row in rows:
        text = f"{row['title']}. {row.get('summary') or ''}".strip()

        try:
            embedding = openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            ).data[0].embedding

            supabase.table("articles")\
                .update({"embedding": embedding})\
                .eq("id", row["id"])\
                .execute()

        except Exception as e:
            print(f"Failed to embed article {row['id']}: {e}")
            continue

        time.sleep(0.1)  # mild rate limiting

    print("Embedding complete.")

if __name__ == "__main__":
    main()
