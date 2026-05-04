from model import train_models

models, vectorizer, results = train_models()

for model, scores in results.items():
    print(f"\n{model}")
    for k, v in scores.items():
        print(f"{k}: {v:.2f}")