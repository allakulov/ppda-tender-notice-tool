import requests
import json
import logging
from datetime import datetime
import pandas as pd

def fetch_data(timeout=120):
    """Fetch data from API or load from backup"""
    url = "https://gpp.ppda.go.ug/adminapi/public/api/tender/notices"
    try:
        request = requests.get(url, timeout=timeout)
        content = request.json()
        # Save backup
        with open('tenders_raw.json', 'w') as f:
            json.dump(content, f)
        return content
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        try:
            with open('tenders_raw.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("No data available: couldn't fetch and no backup found")

def get_stats(df):
    """Get basic statistics about the dataset"""
    today = datetime.now()
    df['deadline_dt'] = pd.to_datetime(df['deadline'], errors='coerce')
    
    stats = {
        'total': len(df),
        'valid_dates': df['deadline_dt'].notna().sum(),
        'future_dates': len(df[df['deadline_dt'] > today]),
        'invalid_dates': df['deadline_dt'].isna().sum()
    }
    return stats