# Tender notice search tool

A semantic search tool for Uganda's public procurement tender notices using sentence transformers to enable semantic similarity search across tender notices.

## Features
- Downloads tender data from Uganda Public Procurement API
- Creates embeddings using sentence-transformers
- Filters by financial year
- Enables semantic search using available data from tender notices
- Configurable number of results and similarity threshold

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

2. Install required packages:
```bash
pip install requests pandas sentence-transformers
```

3. Download data and create embeddings:
```python
python main.py
```

## Usage
After initial setup and running main.py, use the Python terminal (or type python3 in your terminal) and run the following commands:

```python
# Import functions
from main import load_saved_data, search_tenders

# Load saved data - year parameter can be adjusted depending on what was chosen to create embeddings
df, model, embeddings = load_saved_data(year="2024-2025")

# example search 
search_tenders("landscaping", df, model, embeddings, top_k=10, threshold=0.2)
```

Parameters:
- `query`: Search term
- `top_k`: Number of results to return (default=5)
- `threshold`: Minimum similarity score 0-1 (default=0.3)

## Example Output
```
search results for: 'landscaping'

 total matches above threshold 0.2: 54

 showing top 10 results:

Title: Tree planting,weeding,and beating up along 17.4 km roads in Nyaravur-Angal and Parombo Towncouncils in Nebbi District
Type: Non-Consultancy Services
Entity: Nebbi District Local Government
Value: 60000000
Year: 2024-2025
Deadline: 2024-08-30 00:00:00
Title: Rountine Maintenance of Flower Gradens, Sweeping of Town and Road Verges in Division A
Type: Non-Consultancy Services
Entity: Entebbe Municipal Council
Value: 36000000
Year: 2024-2025
Deadline: 2024-07-17 00:00:00
Title: Rountine Maintenance of Flower Gradens, Sweeping of Town and Road Verges in Division A
Type: Non-Consultancy Services
Entity: Entebbe Municipal Council
Value: 36000000
Year: 2024-2025
```

## Notes
- First run will download data from the api, the sentence-transformer model and then create embeddings - this can take a few minutes
- Data is saved locally after first download:
  - `tenders_raw.json`: Raw API data
  - `tenders_2024-2025.csv`: Filtered tender data
  - `embeddings_2024-2025.pkl`: Computed embeddings

The similarity score ranges from -1 to 1:
- 1: Perfect match
- 0: No similarity
