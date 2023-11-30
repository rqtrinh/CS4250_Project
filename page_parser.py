import json

import nltk
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

backup_target_urls = ['https://www.cpp.edu/faculty/alas',
                          'https://www.cpp.edu/faculty/parensburger/index.shtml',
                          'https://www.cpp.edu/faculty/nebuckley/',
                          'https://www.cpp.edu/faculty/jear/index.shtml',
                          'https://www.cpp.edu/faculty/junjunliu/',
                          'https://www.cpp.edu/faculty/jaysonsmith/index.shtml',
                          'https://www.cpp.edu/faculty/jcsnyder/index.shtml',
                          'https://www.cpp.edu/faculty/adsteele/',
                          'https://www.cpp.edu/faculty/aavaldes/index.shtml']


class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def connectDatabase():
    DB_NAME = "project"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db

    except:
        print("Database not connected successfully")


def preprocess_text(text_list, vectorizer):
    vectorizer.fit(text_list)
    return (vectorizer.vocabulary_)


def store_text(db, url, text):
    try:
        # print(json.dumps(text))
        db.parsed_pages.insert_one({'_id': url, 'words': text, 'encoded_vector_shape':text.shape, 'encoded_vector_array':text.toarray()})
    except Exception as e:
        print("error: ", e)


def get_page_as_html(url, db):
    text = []
    page = db.pages.find_one({'_id': url}).get('text')
    bs = BeautifulSoup(page, "html.parser")
    ul_html_data = bs.find_all("ul", {"style": "list-style-type: disc;"})
    for li in ul_html_data:  # handles alas site
        for span in li:
            # print(span.text)
            text.append(span.text)

    html_data = bs.find_all("div", {'class': 'col'})
    for span in html_data:
        # print(span.text)
        text.append(span.text)
    return text

def parse_pages(target_urls):
    stop_words = set(stopwords.words('english'))
    # url = "https://www.cpp.edu/faculty/jaysonsmith/index.shtml"

    db = connectDatabase()
    vectorizer = CountVectorizer(tokenizer=LemmaTokenizer())

    for url in target_urls:
        text_data = []
        page_content = get_page_as_html(url, db)
        for text in page_content:
            text_data.append(text)
        processed_text = preprocess_text(text_data, vectorizer)
        store_text(db, url, processed_text)

#
