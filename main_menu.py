import sys
import scraper 
import index_creator
import ranker
import os 
from scraper import scrape
from index_creator import create_index
from ranker import rank_and_query

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')

def main_menu():
    while True:
        print("\nSearch Engine Main Menu:")
        print("1. Start Web Scraper")
        print("2. Create Index")
        print("3. Search Documents")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # Start the web scraping process
            print("Starting Web Scraper...")
            start_scraping()
        elif choice == '2':
            # Create Index
            print("Create Index")
            create_inverted_index()
        elif choice == '3':
            # Search Documents
            query = [input("Enter search query: ")]
            search_documents(query)
        elif choice == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice, please enter a number between 1-4.")

def start_scraping():
    print("Web scraping started... ")
    #web scrapes for docs, parses them
    scrape()

def create_inverted_index():
    print("Creating inverted index... ")
    create_index()

def search_documents(query):    
    
    # Clear screen 
    clear_screen()

    print(f"Searching for '{query[0]}'... ")
  

    #grab sorted ranked docs
    sorted_ranked_docs = rank_and_query(query)

    #filter out the docs that don't meet the minimum score
    minimum_score = .01
    filtered_docs = list(filter(lambda doc : doc[0] >= minimum_score, sorted_ranked_docs))

    #get just the urls in that order
    retrieved_urls = list(map(lambda doc: doc[1], filtered_docs))

    #group urls into groups of five
    grouped_urls = []       
    for i in range(0, len(retrieved_urls), 5):
        grouped_urls.append(retrieved_urls[i:i+5])

    #current index of page
    page_index = 0

    #err message
    err = ""
    while True: 
        clear_screen()
        print(err) if len(err) > 0 else None

        print("You are on page", page_index  + 1)
        print("1: Previous Page\n"
              "2: Next Page\n"
              "3: Exit\n")
        
        print("Results\n")
        
        #print pages line by line
        if(len(grouped_urls) > 0):
            for url in grouped_urls[page_index]:
                print(url)

        
        choice = input("Enter Key: ")

        if choice == '1':
            if page_index > 0: 
                page_index -=1 
                err = ""
            else:
                err = "You're already on the first page"
        elif choice == '2':
            if page_index < len(grouped_urls) -1:
                page_index +=1 
                err = ""
            else:
                err = "You're already on the last page"
        elif choice == '3':      
            clear_screen()
            break
 



if __name__ == "__main__":
    main_menu()
