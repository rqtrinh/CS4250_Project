# Starting off with template from HW#3
import page_parser
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

target_url = []
# Implementing frontier class to fufill algorithm
class Frontier:
    def __init__(self):
        self.urls = []
    def addURL(self, url):
        self.urls.append(url)
    def nextURL(self):
        if self.urls:
            return self.urls.pop(0)
        return None
    def done(self):
          return not self.urls
    def clear(self):
        self.urls = []
    
# Method to retreive the url returns the html text
def retrieveURL(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), "html.parser")
        return str(bs.get_text)
    except:
        print("Could not open:", url)
        return False

# Store a page in mongo db in pages collection
def storePage(url, html, db):
    try:
        #look if there has an existing entry with this url
        page = db.pages.find_one({'_id': url})
        #if so, update it, otherwise insert
        if(page):
            db.pages.update_one({'_id': url}, {"$set": {"url": url, "text": html }})
        else:
            db.pages.insert_one({'_id': url, 'url': url, 'text': str(html)})
    except:
        print("Error inserting document")

# Checks to see if it is the CS Permanent faculty page
def target_page(html, url):
    try:
        bs = BeautifulSoup(html, "html.parser")
        result = bs.find('div', {'class':'fac-info'})
        if result:
            target_url.append(url)
            return True
        return False
    except:
        print(html)

# Parse the html page for additional links
def parse(html, base):
    bs = BeautifulSoup(html, "html.parser")
    # Find all additional links and add it to the links list
    result = bs.find_all('a', href=True)
    links = []
    for link in result:
        links.append(link['href'])

    # Checking for relative and full links
    # Only want full links so retrieve URL wont crash
    checkHTTPS= re.compile('^https') 
    check_mail =  re.compile('^mailto')

    valid_links = []
    for link in links:
        # If it is a mail link we can ignore it
        if re.match(check_mail, link):
            continue
        # If it is a full link then url is = link
        if re.match(checkHTTPS, link):
            url = link
        else:
        # If it is not we will join the bas link to the relative to create full link
            url = urljoin(base, link)
        # Add full url to valid_links
        valid_links.append(url)
    
    #Return valid links
    return valid_links

# Create database connection using code from previous hw
def connectDataBase():
    # Create a database connection object using pymongo
    # --> add your Python code here
    DB_NAME = "project"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
         client = MongoClient(host=DB_HOST, port=DB_PORT)
         db = client[DB_NAME]
         return db
    
    except:
         print("Database not connected successfully")

# Psuedo code previded 
def crawler_thread(frontier, db, num_targets):
    targets_found = 0
    while not frontier.done():
        url = frontier.nextURL()
        # This html is a string
        html = retrieveURL(url)
        if html == False:
            continue
        storePage(url, html, db)
        # Count found targets
        if target_page(html, url):
            targets_found = targets_found + 1
        if targets_found == num_targets:
            # Implemented clear in frontier class for ease
            frontier.clear()
        else:
            # Passing in url to parse to deal with relative/full links
            for link in parse(html, url):
                frontier.addURL(link)

# Main Program
# Database connection, start link

#scrapes for the 10 urls from biology dept
def scrape():
    db = connectDataBase()
    start = 'https://www.cpp.edu/sci/biological-sciences/index.shtml'

    # Frontier, add start link and use crawler thread.
    frontier = Frontier()
    frontier.addURL(start)
    # I have set it to 10
    crawler_thread(frontier, db, 10)

    # target_url = ['https://www.cpp.edu/faculty/alas', 'https://www.cpp.edu/faculty/parensburger/index.shtml', 'https://www.cpp.edu/faculty/nebuckley/', 'https://www.cpp.edu/faculty/jear/index.shtml', 'https://www.cpp.edu/faculty/junjunliu/', 'https://www.cpp.edu/faculty/ejquestad/index.shtml', 'https://www.cpp.edu/faculty/jaysonsmith/index.shtml', 'https://www.cpp.edu/faculty/jcsnyder/index.shtml', 'https://www.cpp.edu/faculty/adsteele/', 'https://www.cpp.edu/faculty/aavaldes/index.shtml']
    page_parser.parse_pages(target_url)



