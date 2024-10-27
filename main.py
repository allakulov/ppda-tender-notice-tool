import requests
import json
import pandas as pd
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import logging

# show logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# download data
url = "https://gpp.ppda.go.ug/adminapi/public/api/tender/notices"
request = requests.get(url, timeout=120)
content = request.json()
print(content.keys())

#  length of data list
print(f"Number of items in data: {len(content['data'])}")

# latest tender ( orlargest ID value) 
max_id_item = max(content['data'], key=lambda x: x['id'])
print("\nItem with largest ID:")
print(json.dumps(max_id_item, indent=2))

# dataframe
df = pd.DataFrame(content['data'])

# convert to datetime, invalid dates will become NaT 
df['deadline_dt'] = pd.to_datetime(df['deadline'], errors='coerce')

# deadline field analysis
today = datetime.now()
total = len(df)
valid_dates = df['deadline_dt'].notna().sum()
future_dates = len(df[df['deadline_dt'] > today])
invalid_dates = df['deadline_dt'].isna().sum()

print(f"\nDeadline field summary:")
print(f"Total tenders: {total}")
print(f"Valid dates: {valid_dates}")
print(f"Future deadlines: {future_dates}")
print(f"Invalid/empty dates: {invalid_dates}")

# semantic search
def setup_search_engine(content, year="2024-2025"):
    """Initialize the search engine with filtered data"""
    logging.info("starting setup...")
    
    # convert data to DataFrame and filter by year
    logging.info("filtering data...")
    df = pd.DataFrame(content['data'])
    df = df[df['financial_year'] == year]
    
    logging.info(f"found {len(df)} tenders for fiscal year {year}")
    
    # save df to CSV to avoid having to download data
    df.to_csv(f'tenders_{year}.csv', index=False)
    logging.info(f"Saved DataFrame to tenders_{year}.csv")
    
    # load the model
    logging.info("loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # combine all text fields for each row
    logging.info("preparing text data...")
    df['combined_text'] = df.apply(
        lambda x: f"{x['title']} {x['procurement_type']} {x['entity']} "
                 f"{x['sector']} {x['financial_year']} {x['deadline']}", 
        axis=1
    )
    
    # create embeddings
    logging.info("creating embeddings...")
    embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)
    
    # save embeddings
    with open(f'embeddings_{year}.pkl', 'wb') as f:
        pickle.dump(embeddings, f)
    logging.info(f"saved embeddings to embeddings_{year}.pkl")
    
    logging.info("semantic search function is complete!")
    return df, model, embeddings

def load_saved_data(year="2024-2025"):
    """Load saved data"""
    df = pd.read_csv(f'tenders_{year}.csv')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    with open(f'embeddings_{year}.pkl', 'rb') as f:
        embeddings = pickle.load(f)
    return df, model, embeddings

def search_tenders(query, df, model, embeddings, top_k=5, threshold=0.3):
    query_embedding = model.encode([query])
    similarities = np.dot(embeddings, query_embedding.T).squeeze()
    
    # Get indices where similarity is above threshold
    above_threshold = similarities > threshold
    
    # Sort these indices by similarity
    matching_indices = similarities.argsort()
    matching_indices = matching_indices[similarities[matching_indices] > threshold]
    top_indices = matching_indices[-top_k:][::-1]  # Get top k, reversed to show highest first
    
    print(f"\n search results for: '{query}'")
    print(f"\n total matches above threshold {threshold}: {sum(above_threshold)}")
    print(f"\n showing top {min(top_k, len(top_indices))} results:\n")
    
    for idx in top_indices:
        print(f"Title: {df.iloc[idx]['title']}")
        print(f"Type: {df.iloc[idx]['procurement_type']}")
        print(f"Entity: {df.iloc[idx]['entity']}")
        print(f"Value: {df.iloc[idx]['estimatedValue']}")
        print(f"Year: {df.iloc[idx]['financial_year']}")
        print(f"Deadline: {df.iloc[idx]['deadline']}")

# Initialize the search engine
df, model, embeddings = setup_search_engine(content, year="2024-2025")

# how to use from terminal
# from main import load_saved_data, search_tenders
# df, model, embeddings = load_saved_data(year="2024-2025")
# search_tenders("landscaping", df, model, embeddings, top_k=10, threshold=0.2)