from google.cloud import bigquery
from datetime import datetime, UTC
from dotenv import load_dotenv

def load_articles(articles: list[dict], project_name : str, dataset_name : str):
    load_dotenv()
    client = bigquery.Client(project = project_name)
    table_id = f"{project_name}.{dataset_name}.raw_articles"
    
    rows_to_insert = []
    for article in articles:
        rows_to_insert.append({
            "url" : article.get("url") or "N/A",
            "source" : article.get("source").get("name") or "N/A",
            "author" : article.get("author") or "N/A",
            "ingested_at" : datetime.now(UTC).isoformat(),
            "published" : article.get("publishedAt") or "N/A",
            "title" : article.get("title") or "N/A",
            "description" : article.get("description") or "N/A",
            "content" : article.get("content") or "N/A"
        })
    
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("Rows have been added")
    else:
        print(f"Encountered errors while inserting rows: {errors}")
    