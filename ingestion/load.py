from google.cloud import bigquery
from datetime import datetime

def load_articles(articles: list[dict], project_name : str, dataset_name : str):
    client = bigquery.Client(project = project_name)
    table_id = f"{project_name}.{dataset_name}.raw_articles"
    
    rows_to_insert = []
    for article in articles:
        rows_to_insert.append({
            "url" : article.get("url"),
            "source" : article["source"]["name"],
            "author" : article.get("author"),
            "ingested_at" : datetime.now(),
            "published" : article.get("publishedAt"),
            "title" : article.get("title"),
            "description" : article.get("description"),
            "content" : article.get("content") 
        })
    
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors == []:
        print("Rows have been added")
    else:
        print(f"Encountered errors while inserting rows: {errors}")
    