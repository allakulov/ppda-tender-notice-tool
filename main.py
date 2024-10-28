import logging
from data_loader import fetch_data, get_stats
from search_engine import TenderSearchEngine

def print_results(results, total_matches):
    """Print search results"""
    print(f"\nFound {total_matches} matches above threshold")
    print(f"Showing top {len(results)} results:\n")
    
    for result in results:
        print(f"\nScore: {result['score']:.3f}")
        print(f"Title: {result['title']}")
        print(f"Type: {result['type']}")
        print(f"Entity: {result['entity']}")
        print(f"Value: {result['value']}")
        print(f"Year: {result['year']}")
        print(f"Deadline: {result['deadline']}")
        print("- " * 40)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    # Initial setup
    print("Initializing tender search engine...")
    content = fetch_data()
    
    while True:
        print("\n Tender search is now live. Start by selecting a fiscal year, then proceed to search or see stats")
        print("1. Select fiscal year (e.g., 2024-2025)")
        print("2. Search tenders")
        print("3. Show statistics")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            year = input("Enter fiscal year (e.g., 2024-2025): ")
            try:
                search_engine = TenderSearchEngine(content, year)
                print(f"\nSwitched to fiscal year: {year}")
                stats = get_stats(search_engine.df)
                print(f"\nStatistics for {year}:")
                print(f"Total tenders: {stats['total']}")
                print(f"Future deadlines: {stats['future_dates']}")
            except Exception as e:
                print(f"Error: {e}")
                continue
                
        elif choice == '2':
            if not 'search_engine' in locals():
                print("Please select a fiscal year first")
                continue
                
            query = input("Enter search term: ")
            top_k = int(input("Number of results to show (default 5): ") or "5")
            threshold = float(input("Minimum similarity score 0-1 (default 0.3): ") or "0.3")
            
            search_engine.search_tenders(query, top_k, threshold)  
            
        elif choice == '3':
            if not 'search_engine' in locals():
                print("Please select a fiscal year first")
                continue
                
            stats = get_stats(search_engine.df)
            print(f"\nStatistics for {search_engine.year}:")
            print(f"Total tenders: {stats['total']}")
            print(f"Valid deadline dates: {stats['valid_dates']}")
            print(f"Invalid/empty deadline dates: {stats['invalid_dates']}")
            print(f"Future deadlines: {stats['future_dates']}")
            
        elif choice == '4':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()