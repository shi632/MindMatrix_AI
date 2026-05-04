import csv
import random

# Phrases mimicking real PHQ-9, GAD-7, and clinical data
templates = {
    "depression": [
        "I feel so sad and {}",
        "I have lost interest in {}",
        "I am feeling very {} these days",
        "It's hard to get out of bed because I feel {}",
        "I feel {} and hopeless about the future",
        "Everything feels so {}",
        "I constantly feel {} and tired",
        "There is a deep sense of {}",
        "I am {}",
        "I have been feeling {} for weeks"
    ],
    "anxiety": [
        "I am always {}",
        "I can't stop {}",
        "My heart races and I feel {}",
        "I have a lot of {} and fear",
        "I feel {} about everything",
        "I am constantly {} and on edge",
        "I get {} for no reason",
        "I suffer from {} and panic attacks",
        "I feel extremely {}"
    ],
    "stress": [
        "I am feeling extremely {}",
        "My workload is {}",
        "I have too much {} in my life",
        "I can't cope with this {}",
        "Everything is very {}",
        "I feel {} because of exams",
        "The pressure is {}",
        "I am dealing with {}"
    ],
    "normal": [
        "I feel {} today",
        "Everything is {}",
        "I am quite {} right now",
        "Life is {}",
        "I am feeling {} and relaxed",
        "Things are {}"
    ]
}

words = {
    "depression": ["down", "depressed", "worthless", "empty", "gloomy", "miserable", "lonely", "hopeless", "sad", "numb", "exhausted"],
    "anxiety": ["anxious", "worried", "nervous", "panicked", "scared", "fearful", "uneasy", "restless", "terrified", "worrying"],
    "stress": ["stressed", "overwhelmed", "pressured", "hectic", "tiring", "burdened", "frustrating", "demanding", "exhausting"],
    "normal": ["happy", "fine", "good", "great", "okay", "calm", "peaceful", "content", "cheerful", "positive"]
}

# Generate 1500 rows
dataset = []
for label in templates.keys():
    for _ in range(400): # 400 per class = 1600 total
        t = random.choice(templates[label])
        w = random.choice(words[label])
        if "{}" in t:
            sentence = t.format(w)
        else:
            sentence = t
        
        # Add some random noise/extra words to make it look real
        prefix = random.choice(["Lately, ", "Honestly, ", "I think ", "", "", ""])
        suffix = random.choice([" man.", "...", ".", " right now.", " to be honest.", "", ""])
        
        dataset.append([prefix + sentence + suffix, label])

# Write to CSV
with open('data/dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(dataset)

print("Generated realistic dataset with 1600 rows.")
