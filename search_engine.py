# search_engine.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import logging
from sentence_transformers import util

class TenderSearchEngine:
    def __init__(self, content=None, year="2024-2025"):
        self.year = year
        if content:
            self.df, self.model, self.embeddings = self._setup_search_engine(content)
        else:
            self.df, self.model, self.embeddings = self._load_saved_data()
    
    def _setup_search_engine(self, content):
        """Initialize the search engine with filtered data"""
        logging.info("Starting setup...")
        
        # Filter data
        df = pd.DataFrame(content['data'])
        df = df[df['financial_year'] == self.year]
        logging.info(f"Found {len(df)} tenders for {self.year}")
        
        # Save filtered data
        df.to_csv(f'tenders_{self.year}.csv', index=False)
        
        # Setup model and embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')
        df['combined_text'] = df.apply(
            lambda x: f"{x['title']} {x['procurement_type']} {x['entity']} "
                     f"{x['sector']} {x['financial_year']} {x['deadline']}", 
            axis=1
        )
        
        embeddings = model.encode(df['combined_text'].tolist(), 
                                  show_progress_bar=True, 
                                  normalize_embeddings=True)
        with open(f'embeddings_{self.year}.pkl', 'wb') as f:
            pickle.dump(embeddings, f)
            
        return df, model, embeddings
    
    def _load_saved_data(self):
        """Load previously saved data"""
        df = pd.read_csv(f'tenders_{self.year}.csv')
        model = SentenceTransformer('all-MiniLM-L6-v2')
        with open(f'embeddings_{self.year}.pkl', 'rb') as f:
            embeddings = pickle.load(f)
        return df, model, embeddings


    def search_tenders(self, query, threshold=0.3):
        """Search for tenders using semantic search and return results above threshold"""
        
        query_embedding = self.model.encode([query], convert_to_tensor=True)

        top_k = len(self.embeddings)

        hits = util.semantic_search(
            query_embedding, 
            self.embeddings, 
            top_k=top_k, 
            score_function=util.dot_score
        )[0]  

        # apply threshold
        results = [hit for hit in hits if hit['score'] >= threshold]

        # get matching tenders
        matching_indices = [hit['corpus_id'] for hit in results]
        scores = [hit['score'] for hit in results]

        results_df = self.df.iloc[matching_indices].copy()
        results_df['similarity_score'] = scores

        return results_df, len(results_df)
