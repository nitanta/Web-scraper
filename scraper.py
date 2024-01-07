import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from urllib.parse import urlparse, urljoin
from nepalitokenizers import WordPiece
# importing from the HuggingFace tokenizers package
from tokenizers.processors import TemplateProcessing

# keywords = ["समाचार", "आम निर्वाचन २०७९", "विचार", "राजनीति"]
keywords = ["समाचार"]

def setopati(query):
    # Search from 2023 to 2024
    url = f'https://www.setopati.com/search?from=2023%2F01%2F01&to=2024%2F01%2F01&keyword={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    newsContainer = soup.find("div", {"class": "row bishesh news-cat-list video-list search-res-list"})
    articles = newsContainer.find_all("div", {"class": "items col-md-4"})

    newslist = []

    for item in articles:
        newsarticle = {
            'title': item.find('span', {"class": "main-title"}).get_text(),
            'link': item.find('a', href=True).get('href')
        }
        newslist.append(newsarticle)
    return newslist

def onlinekhabar(query):
    # Normal Search
    url = f'https://www.onlinekhabar.com/?search_keyword={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("div", {"class": "ok-news-post ok-post-ltr"})

    newslist = []
    for item in articles:
        newsarticle = {
            'title': item.find('h2').get_text(),
            'link': item.find('a', href=True).get('href')
        }
        newslist.append(newsarticle)
    return newslist

def ratopati(query):
    # Normal Search
    url = f'https://www.ratopati.com/search?query={query}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("div", {"class": "columnnews mbl-col col3"})

    newslist = []

    for item in articles:
        newsarticle = {
            'title': item.find('h3').get_text(),
            'link': item.find('a', href=True).get('href')
        }
        newslist.append(newsarticle)
    return newslist

def kantipur(query):
    # Search from 2023 to 2024
    url = f'https://ekantipur.com/search/2024/?txtSearch={query}&year=2023&date-from=2024-01-01&date-to=2024-01-01'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("article")

    newslist = []

    base_url = urlparse(url).scheme + '://' + urlparse(url).hostname

    for item in articles:
        titleItem = item.find('h2')
        link = titleItem.find('a', href=True).get('href')
        newsarticle = {
            'title': titleItem.get_text(),
            'link': urljoin(base_url, link)
        }
        newslist.append(newsarticle)

    return newslist

def hamropatro(query):
    url = f'https://www.hamropatro.com/news?q={query}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("div", {"class": "item newsCard"})

    newslist = []

    base_url = urlparse(url).scheme + '://' + urlparse(url).hostname

    for item in articles:
        titleItem = item.find('h2')
        link = titleItem.find('a', href=True).get('href')
        newsarticle = {
            'title': item.find('h2').get_text(),
            'link': urljoin(base_url, link)
        }
        newslist.append(newsarticle)

    return newslist

def fetch_data(query):
    # print(f"*******************{query}***********************")
    combined_data = setopati(query) + onlinekhabar(query) + ratopati(query) + kantipur(query) + hamropatro(query)
    # print(combined_data)
    # print(f"******************************************")
    return combined_data

def load_stop_words(file_path):
    stop_words = []
    try:
        with open(file_path, 'r') as file:
            stop_words = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return stop_words

def preprocess_text(text):
    tokenizer_sp = WordPiece()

    # change the post processor to not add any special tokens
    # treat tokenizer_sp as HuggingFace's Tokenizer object
    tokenizer_sp.post_processor = TemplateProcessing()
    tokens = tokenizer_sp.encode(text)

    print(tokens.tokens)

    stop_words = load_stop_words('nepali.txt')
    print(stop_words)
    # words = [word for word in words if word.lower() not in stop_words]

    # stemmer = SnowballStemmer('nepali')
    # words = [stemmer.stem(word) for word in words]

    # return words

def compute_term_frequencies(words):
    # Compute term frequencies
    term_frequencies = Counter(words)
    return term_frequencies

def plot_term_frequencies(term_frequencies, genre):
    # Plot the top 20 terms
    common_terms = term_frequencies.most_common(20)
    terms, counts = zip(*common_terms)
    
    plt.barh(terms, counts, color='skyblue')
    plt.xlabel('Term Frequency')
    plt.title(f'Top 20 Terms in {genre}')
    plt.show()
    
    # for article in articles:
    #     # Assuming 'text' is the key for the article text
    #     words = preprocess_text(article['text'])
        
    #     for keyword in keywords:
    #         if keyword in words:
    #             # Do something with the article, e.g., analyze sentiment

    #     term_frequencies = compute_term_frequencies(words)
    #     plot_term_frequencies(term_frequencies, genre='News')  # Replace 'News' with the actual genre

# Implement similar logic for political leaders and parties analysis

# for query in keywords:
#     data = fetch_data(query)
#     result_string = ' '.join([item["title"] for item in data])
#     preprocessed_string = preprocess_text(result_string)
#     print(preprocessed_string)
    

stop_words = load_stop_words('nepali.txt')
print(stop_words)
