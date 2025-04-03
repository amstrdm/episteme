#!/usr/bin/env python
"""
Automatic Testing Script for Duplicate Filtering Threshold Evaluation

This script computes cosine similarity between pairs of thesis points using three models:
  - OpenAI's text-embedding-ada-002
  - OpenAI's text-embedding-3-small
  - SentenceTransformer (all-MiniLM-L6-v2)

It iterates over a range of cosine similarity thresholds and compares the predicted duplicate labels 
against a set of ground truth labels (1 = duplicate, 0 = not duplicate). Evaluation metrics (accuracy,
precision, recall, and F1 score) are printed for each model at each threshold, along with average similarity 
values for duplicate and non-duplicate pairs.

This information will enable an unbiased assessment of the optimal threshold and model choice for duplicate filtering.

Ensure you have the required packages installed:
    pip install openai numpy scikit-learn sentence-transformers
Also, set the OPENAI_API_KEY environment variable.
"""

import os
import numpy as np
import openai
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sentence_transformers import SentenceTransformer

# Set OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY ENVIRONMENT VARIABLE IS EITHER EMPTY OR DOESN'T EXIST")
openai.api_key = OPENAI_API_KEY

# Expanded dataset: Test pairs with ground truth labels (1: duplicate, 0: not duplicate)
TEST_PAIRS = [
    { "point1": "EPS grew by 5% year-over-year", "point2": "Earnings increased slightly", "label": 1 },
    { "point1": "Expanded renewable energy capacity", "point2": "Acquired new packaging line for efficient production", "label": 0 },
    { "point1": "EPS grew by 5% year-over-year", "point2": "New cost-saving measures improved margins", "label": 0 },
    { "point1": "Earnings increased slightly", "point2": "Acquired new packaging line for efficient production", "label": 0 },
    { "point1": "EPS grew by 5% year-over-year", "point2": "CEO owns a lot of shares", "label": 0 },
    { "point1": "Revenue increased by 10% in Q2", "point2": "Sales grew 10% in the second quarter", "label": 1 },
    { "point1": "Operating margins improved due to lower expenses", "point2": "Cost-cutting measures led to higher operating margins", "label": 1 },
    { "point1": "The company expanded its market share in Europe", "point2": "European market share increased significantly", "label": 1 },
    { "point1": "Research and development expenses rose modestly", "point2": "R&D costs increased slightly", "label": 1 },
    { "point1": "The new CEO's appointment boosted investor confidence", "point2": "Investors are more confident after the new CEO was hired", "label": 1 },
    { "point1": "Supply chain disruptions impacted production negatively", "point2": "Production suffered due to supply chain issues", "label": 1 },
    { "point1": "Stock buyback program announced for Q3", "point2": "Share repurchase plan to be implemented in the third quarter", "label": 1 },
    { "point1": "The firm's profitability declined sharply", "point2": "The company experienced a severe drop in profits", "label": 1 },
    { "point1": "New product launches are expected to drive future growth", "point2": "Upcoming product releases should boost long-term growth", "label": 1 },
    { "point1": "The company’s debt levels are concerning", "point2": "High leverage is a risk factor for the firm", "label": 1 },
    { "point1": "Customer satisfaction improved according to recent surveys", "point2": "Feedback from recent surveys shows higher customer approval", "label": 1 },
    { "point1": "EPS grew by 5% year-over-year", "point2": "Revenue declined by 2% last quarter", "label": 0 },
    { "point1": "The firm’s new marketing strategy increased brand visibility", "point2": "R&D investments are expected to yield innovation", "label": 0 },
    { "point1": "Operating margins improved due to cost reductions", "point2": "The CEO resigned unexpectedly", "label": 0 },
    { "point1": "Market share in Asia expanded significantly", "point2": "Stock buybacks are planned for next quarter", "label": 0 },
    { "point1": "Quarterly net income grew by 12%", "point2": "Net profits increased by 12% this quarter", "label": 1 },
    { "point1": "Operating income saw a significant uptick", "point2": "There was a notable rise in operating income", "label": 1 },
    { "point1": "The company launched a new smartphone model", "point2": "R&D expenses were cut by 8%", "label": 0 },
    { "point1": "Profit margins improved by 4 percentage points", "point2": "The firm’s profit margin increased by 4%", "label": 1 },
    { "point1": "The board approved a major acquisition", "point2": "Earnings per share increased modestly", "label": 0 },
    { "point1": "Total assets grew due to recent investments", "point2": "Investments contributed to an increase in total assets", "label": 1 },
    { "point1": "The company is expanding its operations in Asia", "point2": "Shareholder dividends were reduced", "label": 0 },
    { "point1": "The merger resulted in cost synergies", "point2": "Cost synergies were achieved post-merger", "label": 1 },
    { "point1": "The company experienced regulatory challenges", "point2": "Revenue increased substantially", "label": 0 },
    { "point1": "Capital expenditures were reduced this year", "point2": "There was a decline in capex in the current year", "label": 1 },
    { "point1": "The firm’s free cash flow improved significantly", "point2": "Free cash flow saw a notable improvement", "label": 1 },
    { "point1": "Customer acquisition costs rose sharply", "point2": "The CEO received a bonus", "label": 0 },
    { "point1": "Earnings before interest and taxes (EBIT) increased", "point2": "EBIT showed a clear upward trend", "label": 1 },
    { "point1": "The company announced plans for a new factory", "point2": "There were layoffs in the sales department", "label": 0 },
    { "point1": "Shareholder return improved due to dividends and buybacks", "point2": "Return to shareholders increased with higher dividends and repurchases", "label": 1 },
    { "point1": "The company’s market valuation soared", "point2": "Production delays affected output", "label": 0 },
    { "point1": "Return on equity (ROE) improved compared to last year", "point2": "ROE increased year-over-year", "label": 1 },
    { "point1": "The firm is investing in artificial intelligence", "point2": "Cost-cutting measures improved net income", "label": 0 },
    { "point1": "Operating expenses were trimmed effectively", "point2": "The company reduced its operating costs significantly", "label": 1 },
    { "point1": "The firm’s research pipeline remains robust", "point2": "Stock volatility increased after the earnings report", "label": 0 },
    {""}
]

# Function to get OpenAI embeddings using specified model
def get_openai_embedding(text: str, model: str) -> np.array:
    response = openai.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    return np.array(embedding)

# Load local SentenceTransformer model
st_finlang_model = SentenceTransformer("FinLang/finance-embeddings-investopedia")
st_minilm_model = SentenceTransformer("all-MiniLM-L6-v2")

# Compute cosine similarity between two vectors
def compute_cos_sim(vec1: np.array, vec2: np.array) -> float:
    return cosine_similarity([vec1], [vec2])[0][0]

# Compute similarities for each test pair for each embedding model
def compute_similarities():
    results = {}
    models = {
        "ada-002": lambda text: get_openai_embedding(text, "text-embedding-ada-002"),
        "3-small": lambda text: get_openai_embedding(text, "text-embedding-3-small"),
        "MiniLM":  lambda text: st_minilm_model.encode(text),
        "FinLang": lambda text: st_finlang_model.encode(text),
    }
    
    for model_name, embed_func in models.items():
        similarities = []
        for pair in TEST_PAIRS:
            emb1 = embed_func(pair["point1"])
            emb2 = embed_func(pair["point2"])
            sim = compute_cos_sim(emb1, emb2)
            similarities.append(sim)
        results[model_name] = similarities
    return results

# Evaluate predictions based on a threshold for given similarities and ground truth labels.
def evaluate_threshold(similarities: list, threshold: float, labels: list):
    predictions = [1 if sim >= threshold else 0 for sim in similarities]
    acc = accuracy_score(labels, predictions)
    prec = precision_score(labels, predictions, zero_division=0)
    rec = recall_score(labels, predictions, zero_division=0)
    f1 = f1_score(labels, predictions, zero_division=0)
    return {
        "threshold": threshold,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "predictions": predictions
    }

def main():
    # Compute similarities for each model
    similarities = compute_similarities()
    
    # Ground truth labels for test pairs
    labels = [pair["label"] for pair in TEST_PAIRS]
    
    # Define a range of thresholds (from 0.1 to 0.9 with step 0.05)
    thresholds = np.arange(0.1, 0.91, 0.05)
    
    evaluation_summary = {}
    for model_name, sims in similarities.items():
        model_results = []
        for thresh in thresholds:
            metrics = evaluate_threshold(sims, thresh, labels)
            model_results.append(metrics)
        evaluation_summary[model_name] = model_results
        
        # Calculate average similarity for duplicate and non-duplicate pairs
        dup_sims = [sim for sim, pair in zip(sims, TEST_PAIRS) if pair["label"] == 1]
        nondup_sims = [sim for sim, pair in zip(sims, TEST_PAIRS) if pair["label"] == 0]
        avg_dup = np.mean(dup_sims) if dup_sims else None
        avg_nondup = np.mean(nondup_sims) if nondup_sims else None
        
        print(f"\nModel: {model_name}")
        print(f"  Average similarity for duplicate pairs: {avg_dup:.3f}")
        print(f"  Average similarity for non-duplicate pairs: {avg_nondup:.3f}")
        print("Threshold | Accuracy | Precision | Recall | F1 Score")
        for res in model_results:
            print(f"  {res['threshold']:.2f}      |  {res['accuracy']:.3f}   |  {res['precision']:.3f}    |  {res['recall']:.3f} |  {res['f1']:.3f}")
        
if __name__ == "__main__":
    main()
