from google.cloud import bigquery
from transformers import pipeline
from dotenv import load_dotenv

def score(project_name : str, dataset_name : str):
    load_dotenv()
    sentiment_pipeline = pipeline(model = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    client = bigquery.Client(project = project_name)
    table_id_raw = f"{project_name}.{dataset_name}.raw_articles"
    table_id_sentiment = f"{project_name}.{dataset_name}.raw_articles_sentiment"
    
    QUERY = (
        f"""SELECT r.url, r.title, r.description, r.content 
        FROM `{table_id_raw}` as r
        WHERE r.url NOT IN (SELECT s.url 
            FROM `{table_id_sentiment}` as s WHERE s.url IS NOT NULL);"""
             )
    
    query_job = client.query(QUERY)
    rows = query_job.result()
    
    for row in rows:
        # print(list(row)[0])
        scores = sentiment_pipeline(list(row))
        print(scores)
                
score(project_name= "news-sentiment-analysis-499303", dataset_name= "news_sentiment_raw")