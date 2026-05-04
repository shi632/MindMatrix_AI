import re

# Define keyword lists for various symptom categories
STRESS_KEYWORDS = [
    'stress', 'overwhelm', 'pressure', 'burnout', 'exhausted', 'cant cope',
    'overload', 'exam', 'deadline', 'assignment', 'tension', 'anxiety'
]
ANXIETY_KEYWORDS = [
    'anxious', 'anxiety', 'worried', 'worry', 'panic', 'nervous', 'fear',
    'scared', 'overthink', 'racing heart', 'restless'
]
DEPRESSION_KEYWORDS = [
    'depress', 'sad', 'hopeless', 'empty', 'worthless', 'crying', 'cry',
    'give up', 'no point', 'lost interest', 'numb', 'miserable', 'unhappy',
    'low mood', 'feeling down'
]

def _count_keywords(text: str, keywords: list) -> int:
    """Count occurrences of any keyword in the given text (case‑insensitive)."""
    lowered = text.lower()
    count = 0
    for kw in keywords:
        # Use word boundaries to avoid partial matches
        pattern = r"\\b" + re.escape(kw) + r"\\b"
        count += len(re.findall(pattern, lowered))
    return count

def compute_score(text: str) -> int:
    """Compute a simple integer score based on symptom keyword frequencies.

    The scoring logic is intentionally lightweight – each occurrence of a stress‑related
    keyword adds 2 points, anxiety keywords add 1 point, and depression keywords add 3
    points. The total is returned as an integer.
    """
    stress_score = _count_keywords(text, STRESS_KEYWORDS) * 2
    anxiety_score = _count_keywords(text, ANXIETY_KEYWORDS) * 1
    depression_score = _count_keywords(text, DEPRESSION_KEYWORDS) * 3
    return stress_score + anxiety_score + depression_score

def classify_score(score: int) -> str:
    """Classify the numeric score into a human‑readable stress level.

    - Score < 5   → "Normal"
    - 5 ≤ Score ≤ 10 → "Mild Stress"
    - Score > 10 → "High Stress"
    """
    if score < 5:
        return "Normal"
    if 5 <= score <= 10:
        return "Mild Stress"
    return "High Stress"
