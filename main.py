import logging
from data_loader import fetch_data, get_stats
from search_engine import TenderSearchEngine
import pandas as pd
from tabulate import tabulate


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
            
            #  all search results above threshold
            results_df, total_matches = search_engine.search_tenders(query, threshold=threshold)
            
            # top_k results initially
            display_df = results_df.head(top_k)[['entity', 'title', 'sector', 'procurement_type', 'similarity_score']]
            
            print(f"\nSearch results for: '{query}'")
            print(f"Total matches above threshold {threshold}: {total_matches}")
            print(f"\nShowing top {top_k} results:")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
            
            # Filter menu 
            while True:
                print("\nWould you like to filter these results?")
                print("1. Filter by procurement type")
                print("2. Back to main menu")
                
                filter_choice = input("\nEnter choice (or press Enter to go back): ")
                
                if filter_choice == "1":
                    types = results_df['procurement_type'].unique()
                    print("\nAvailable procurement types:")
                    for i, ptype in enumerate(types, 1):
                        count = len(results_df[results_df['procurement_type'] == ptype])
                        print(f"{i}. {ptype} ({count} tenders)")
                    
                    type_choice = input("\nSelect procurement type number (or press Enter to go back): ")
                    if type_choice.strip():
                        try:
                            type_idx = int(type_choice) - 1
                            if 0 <= type_idx < len(types):
                                filtered_df = results_df[results_df['procurement_type'] == types[type_idx]]
                                display_df = filtered_df[['entity', 'title', 'sector', 'procurement_type', 'estimatedValue']]
                                print(f"\nFiltered results for {types[type_idx]}:")
                                print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
                            else:
                                print("Invalid choice")
                        except ValueError:
                            print("Please enter a valid number")
                
                elif not filter_choice or filter_choice == "2":
                    break

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