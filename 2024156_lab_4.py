#task 1

import string

def clean_text(text, stopwords):
    # Remove punctuation marks
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert text to lowercase
    text = text.lower()
    # Split text into individual words
    words = text.split()
    # Eliminate stopwords from the text
    filtered_words = [word for word in words if word not in stopwords]
    return filtered_words

def calculate_word_frequencies(words):
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def get_most_frequent_words(word_counts):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:5]

def main():
    stopwords = {"the", "a", "an", "is", "are", "it", "that", "this", "these", "those",
                 "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them",
                 "my", "your", "his", "her", "our", "their", "mine", "yours", "hers", "ours", "theirs",
                 "and", "but", "or", "nor", "for", "so", "yet", "as", "while", "since", "because",
                 "in", "on", "at", "by", "with", "about", "against", "through", "during", "before", "after",
                 "to", "from", "of", "at", "into", "throughout", "among", "between", "over", "under",
                 "have", "has", "had", "do", "does", "did", "will", "would", "can", "could", "should", "may", "might", "must",
                 "be", "being", "been", "am", "is", "are", "was", "were",
                 "not", "no", "nor", "neither", "never", "always", "sometimes", "often", "usually", "generally"}
    
    text = input("Enter a paragraph of text: ")
    words = clean_text(text, stopwords)
    word_counts = calculate_word_frequencies(words)
    
    print("\nTop 5 most frequent words:")
    for word, count in get_most_frequent_words(word_counts):
        print(f"{word}: {count}")
    
    uppercase_words = list(map(str.upper, words))
    print("\nWords in uppercase:", uppercase_words)
    
    common_words = list(filter(lambda w: word_counts[w] > 2, word_counts))
    print("\nWords appearing more than twice:", common_words)
    
    vowels = {'a', 'e', 'i', 'o', 'u'}
    vowel_words = list(filter(lambda w: w[0] in vowels, word_counts))
    print("\nWords starting with a vowel:", vowel_words)

main()

#task 2

square_add_five = lambda x: (x ** 2) + 5
num = int(input("Enter a number: "))
print("Result:", square_add_five(num))