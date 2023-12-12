from bs4 import BeautifulSoup
from pymongo import MongoClient
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

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

        #try to update if entry exists, update otherwise
        parsed_page = db.parsed_pages.find_one({'_id': url})
        if(parsed_page):
            db.parsed_pages.update_one({'_id': url}, {"$set": {'words': text}})
        else:
            db.parsed_pages.insert_one({'_id': url, 'words': text})
    except Exception as e:
        print("error: ", e)


def get_page_as_html(url, db):
    text = []
    # div class "blurb"
    # div class:"section-intro"
    # div class="section-text" : has the header info
    # div class="section-menu" > div class="col" has text in h2, p, span

    page = db.pages.find_one({'_id': url}).get('text') # Get a page from the database
    bs = BeautifulSoup(page, "html.parser")

    section_intro_data = bs.find_all("div", {"class": "blurb"})
    side_panel_data = bs.find_all("div", {"class": "accolades"})
    for element in section_intro_data:
        # print("Element from blurb: ", element.text)
        text.append(element.text)

    for elem in side_panel_data:
        # print ("Element from side panel: ", elem.text)
        text.append(elem.text)

    return text

def parse_pages(target_urls):
    stop_words = set(stopwords.words('english'))
    stop_words.add('\n')
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


parse_pages("")