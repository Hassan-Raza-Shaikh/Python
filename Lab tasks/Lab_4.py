#Task 1

import string

def preprocess_text(text, stopwords):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    # Split into words
    words = text.split()
    # Remove stopwords
    filtered_words = [word for word in words if word not in stopwords]
    return filtered_words

def count_word_frequencies(words):
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

def get_top_five_words(frequency):
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
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
    words = preprocess_text(text, stopwords)
    frequency = count_word_frequencies(words)
    
    print("\nTop 5 most frequent words:")
    for word, count in get_top_five_words(frequency):
        print(f"{word}: {count}")
    
    uppercase_words = list(map(str.upper, words))
    print("\nWords in uppercase:", uppercase_words)
    
    frequent_words = list(filter(lambda w: frequency[w] > 2, frequency))
    print("\nWords appearing more than twice:", frequent_words)
    
    vowels = {'a', 'e', 'i', 'o', 'u'}
    vowel_words = list(filter(lambda w: w[0] in vowels, frequency))
    print("\nWords starting with a vowel:", vowel_words)

#if __name__ == "__main__":
main()


#Task 2

square_add_five = lambda x: (x ** 2) + 5

num = int(input("Enter a number: "))
print("Result:", square_add_five(num))
