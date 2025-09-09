import re
import json

def load_stopwords(filepath):
    """Load stopwords from a JSON file and return them as a set."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return set(json.load(file))

def clean_text(text):
    """Normalize text by converting it to lowercase and removing non-alphabetic characters."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def remove_stopwords(text, stopwords):
    """Filter out stopwords from the given text and return a set of unique words."""
    words = text.split()
    return {word for word in words if word not in stopwords}

def jaccard_similarity(set1, set2):
    """Compute the Jaccard similarity score between two sets."""
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0 

def calculate_text_similarity(file1, file2, stopwords_file):
    """Compare two text files and return their Jaccard similarity score."""
    stopwords = load_stopwords(stopwords_file)

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        text1 = clean_text(f1.read())
        text2 = clean_text(f2.read())

    word_set1 = remove_stopwords(text1, stopwords)
    word_set2 = remove_stopwords(text2, stopwords)

    return jaccard_similarity(word_set1, word_set2)

file1_path = 'michelle_obama_speech.txt'
file2_path = 'melina_trump_speech.txt'
stopwords_path = 'stop_words.txt'

similarity = calculate_text_similarity(file1_path, file2_path, stopwords_path)
print(f"Jaccard Similarity Score: {similarity:.4f}")
