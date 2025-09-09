import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Scrape data from the website
url = "http://quotes.toscrape.com/"
quotes = []
authors = []
tags_list = []

while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes_data = soup.find_all("div", class_="quote")
    for quote in quotes_data:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        
        quotes.append(text)
        authors.append(author)
        tags_list.append(", ".join(tags))

    # Get next page URL
    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_link = next_btn.find("a")["href"]
        url = f"http://quotes.toscrape.com{next_link}"
    else:
        url = None

# Step 2: Store in a DataFrame
df = pd.DataFrame({
    "Quote": quotes,
    "Author": authors,
    "Tags": tags_list
})

# Step 3: Clean the data
df["Quote"] = df["Quote"].str.replace('“|”', '', regex=True).str.strip()
df["Author"] = df["Author"].str.strip()

# Step 4: Analysis

# 1. Most frequent author
most_frequent_author = df["Author"].value_counts().idxmax()
print(f"Most quoted author: {most_frequent_author}")

# 2. Average quote length
df["Quote Length"] = df["Quote"].apply(len)
average_length = df["Quote Length"].mean()
print(f"Average quote length: {average_length:.2f} characters")

# 3. Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 4. Visualization (quote length by top 5 authors)
top_authors = df["Author"].value_counts().head(5).index
filtered_df = df[df["Author"].isin(top_authors)]
plt.figure(figsize=(10, 6))
filtered_df.boxplot(column="Quote Length", by="Author")
plt.title("Quote Length by Top 5 Authors")
plt.suptitle("")
plt.ylabel("Length (characters)")
plt.xlabel("Author")
plt.show()

# 5. Reflection questions
print("\nReflection:")
print("a. Challenge: Handling pagination and selecting clean HTML tags for scraping.")
print("b. The HTML was easy to navigate because it was well-structured.")
print("c. This data could be useful for NLP tasks, analyzing sentiment, or understanding author influence.")


# Example usage of the requests library
# response = requests.get('https://api.github.com')
# if response.status_code == 200:
#     print("Request was successful!")
#     print(response.json())
# else:
#     print(f"Request failed with status code: {response.status_code}")