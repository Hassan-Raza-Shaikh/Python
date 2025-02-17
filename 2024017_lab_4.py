#task 1

import string

def preprocess_text(text, stopwords):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    # Split into words
    words = text.split()
    # Remove stopwords
    words = [word for word in words if word not in stopwords]
    return words

def count_word_frequencies(words):
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq

def top_five_words(word_freq):
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:5]

def main():
    stopwords = [
        "the", "a", "an", "is", "are", "it", "that", "this", "these", "those",
        "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them",
        "my", "your", "his", "her", "our", "their", "mine", "yours", "hers", "ours", "theirs",
        "and", "but", "or", "nor", "for", "so", "yet", "as", "while", "since", "because",
        "in", "on", "at", "by", "with", "about", "against", "through", "during", "before", "after",
        "to", "from", "of", "at", "into", "throughout", "among", "between", "over", "under",
        "have", "has", "had", "do", "does", "did", "will", "would", "can", "could", "should", "may", "might", "must",
        "be", "being", "been", "am", "is", "are", "was", "were",
        "not", "no", "nor", "neither", "never", "always", "sometimes", "often", "usually", "generally",
        "more", "less", "many", "few", "some", "all", "most", "every", "each", "both", "several",
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"
    ]
    
    text = input("Enter a paragraph of text: ")
    words = preprocess_text(text, stopwords)
    word_freq = count_word_frequencies(words)
    
    print("\nTop 5 most frequent words:")
    for word, count in top_five_words(word_freq):
        print(f"{word}: {count}")
    
    uppercase_words = list(map(str.upper, words))
    print("\nWords in uppercase:", uppercase_words)
    
    words_more_than_twice = list(filter(lambda w: word_freq[w] > 2, word_freq))
    print("\nWords appearing more than twice:", words_more_than_twice)
    
    words_starting_with_vowel = list(filter(lambda w: w[0] in 'aeiou', word_freq))
    print("\nWords starting with a vowel:", words_starting_with_vowel)
    
main()

#task 2

square_add_five = lambda x: x**2 + 5

# Taking user input
num = int(input("Enter a number: "))

# Applying the lambda function
result = square_add_five(num)

# Displaying the result
print(f"Result: {result}")
