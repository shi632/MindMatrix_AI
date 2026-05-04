import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


import pickle
import os
import json

def train_models():
    # Load trained model (.pkl) if it exists
    if os.path.exists("models.pkl") and os.path.exists("vectorizer.pkl") and os.path.exists("model_metadata.json"):
        print("Loading trained models from .pkl files...")
        with open("models.pkl", "rb") as f:
            models = pickle.load(f)
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        with open("model_metadata.json", "r") as f:
            results = json.load(f)
        return models, vectorizer, results
        
    print("Training models...")
    data = pd.read_csv("data/dataset.csv")
    dataset_size = len(data)

    X = data['text']
    y = data['label']

    # TF-IDF
    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42
    )

    # Models
    nb = MultinomialNB()
    gnb = GaussianNB()
    bnb = BernoulliNB()
    lr = LogisticRegression(max_iter=1000)
    svm = SVC(probability=True)

    models = {
        "naive_bayes": nb,
        "gaussian_nb": gnb,
        "bernoulli_nb": bnb,
        "logistic": lr,
        "svm": svm
    }

    results = {"dataset_size": dataset_size, "models": {}}

    # Train + Evaluate
    for name, model in models.items():
        if name == "gaussian_nb":
            model.fit(X_train.toarray(), y_train)
            y_pred = model.predict(X_test.toarray())
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        results["models"][name] = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
            "Recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
            "F1-score": f1_score(y_test, y_pred, average='weighted', zero_division=0)
        }
        
    # Save trained models to .pkl files
    with open("models.pkl", "wb") as f:
        pickle.dump(models, f)
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("model_metadata.json", "w") as f:
        json.dump(results, f)

    print("Models saved successfully to .pkl files.")
    return models, vectorizer, results


import re
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def clean_text(text):
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize and remove stopwords
    words = text.split()
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return " ".join(words)

def predict(text, models, vectorizer):
    processed_text = clean_text(text)
    vec = vectorizer.transform([processed_text])
    
    # Extract important keywords (top 5 by TF-IDF score)
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = vec.toarray()[0]
    top_indices = np.argsort(tfidf_scores)[::-1][:5]
    top_keywords = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0]

    return {
        "processed_text": processed_text,
        "keywords": top_keywords,
        "naive_bayes": models["naive_bayes"].predict(vec)[0],
        "gaussian_nb": models["gaussian_nb"].predict(vec.toarray())[0],
        "bernoulli_nb": models["bernoulli_nb"].predict(vec)[0],
        "logistic": models["logistic"].predict(vec)[0],
        "svm": models["svm"].predict(vec)[0]
    }