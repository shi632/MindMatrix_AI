import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

nltk.download('stopwords')

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()

    words = text.split()

    words = [w for w in words if w not in stop_words]

    words = [ps.stem(w) for w in words if w not in string.punctuation]

    return " ".join(words)