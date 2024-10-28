# Tender Notice Search Tool

A semantic search tool for Uganda's public procurement tender notices using sentence transformers to enable semantic similarity search across tender notices.

## Features
- Downloads tender data from GPP API of Uganda PPDA
- Creates embeddings using sentence-transformers
- Filters by financial year
- Enables semantic search using available data from tender notices
- Interactive CLI interface
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

3. Run the application:
```bash
python main.py
```

## Usage
The tool provides an interactive menu with the following options:
1. Select fiscal year (e.g., 2024-2025)
2. Search tenders
3. Show statistics
4. Exit

### Example Session:
```
Initializing tender search engine...

Tender search is now live. Start by selecting a fiscal year, then proceed to search or see stats
1. Select fiscal year (e.g., 2024-2025)
2. Search tenders
3. Show statistics
4. Exit

Enter your choice (1-4): 1
Enter fiscal year (e.g., 2024-2025): 2023-2024
2024-10-28 21:11:08,047 - Starting setup...
2024-10-28 21:11:08,170 - Found 3596 tenders for 2023-2024
2024-10-28 21:11:08,183 - Use pytorch device_name: mps
2024-10-28 21:11:08,183 - Load pretrained SentenceTransformer: all-MiniLM-L6-v2
Batches: 100%|███████████████████████████████████████████████████████| 113/113 [00:05<00:00, 22.37it/s]

Switched to fiscal year: 2023-2024

Statistics for 2023-2024:
Total tenders: 3596
Future deadlines: 1

Enter your choice (1-4): 2
Enter search term: landscaping
Number of results to show (default 5): 
Minimum similarity score 0-1 (default 0.3): 
Batches: 100%|███████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  4.58it/s]

Search results for: 'landscaping'
Total matches above threshold 0.3: 70
Showing top 5 results:


Title: FENCING  AND LANDSCAPING WORKS FOR MUBENDE BOREHOLE NO.7, UNDER EACOP
Type: Works
Entity: National Water & Sewerage Corporation
Value: 40000000
Year: 2023-2024
Deadline: 2023-07-27 00:00:00
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Title: Routine maintenance of flower gardens, sweeping of town and road verges in Division A
Type: Non-Consultancy Services
Entity: Entebbe Municipal Council
Value: 2000000
Year: 2023-2024
Deadline: 2023-07-12 00:00:00
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Title: Slash weeding in Mwenge Plantations;300ha
Type: Non-Consultancy Services
Entity: National Forestry Authority
Value: 45000000
Year: 2023-2024
Deadline: 2023-11-14 00:00:00
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
...
```

## Notes
- First run will download data from the API and the sentence-transformer model (~90MB)
- Data is saved locally after first download:
  - `tenders_raw.json`: Raw API data
  - `tenders_2024-2025.csv`: Filtered tender data
  - `embeddings_2024-2025.pkl`: Computed embeddings
- Additional csv and pkl files are created for any other fiscal years selected.

Find out more about the all-MiniLM-L6-v2 model here: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2