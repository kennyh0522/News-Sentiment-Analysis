from google.cloud import bigquery
from transformers import pipeline
from dotenv import load_dotenv
from collections import Counter
from datetime import datetime, UTC

def score_articles(project_name : str, dataset_name : str):
    load_dotenv()
    sentiment_pipeline = pipeline("text-classification", model = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
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
    
    
    scores = []
    for row in rows:
        # Row Scoring
        row = list(row)
        scored = sentiment_pipeline(inputs = row) # outputs a list of dictionaries
        scores.append({"url" : row[0], 
                       "title_score" : scored[1]["score"], 
                       "description_score" : scored[2]["score"], 
                       "content_score" : scored[3]["score"], 
                       "compound_score" : calculate_compound(scored),
                       "sentiment_label" : get_sentiment(scored),
                       "scored_at" : datetime.now(UTC).isoformat()
                       })
        
    errors = client.insert_rows_json(table_id_sentiment, scores)
    if errors == []:
        print("Rows have been added")
    else:
        print(f"Encountered errors while inserting rows: {errors}")
        
def calculate_compound(scored : list[dict[str, int]]):
    compound = 0
    for score in scored:
        compound += score["score"]
        
    return compound

def get_sentiment(scored : list[dict[str, int]]):
    sentiments = {"positive" : 0,
                  "neutral": 0,
                  "negative": 0}
    for score in scored:
        score_sentiment = score["label"]
        if score_sentiment in sentiments:
            sentiments[score_sentiment] += 1
    return max(sentiments, key = sentiments.get)
                        