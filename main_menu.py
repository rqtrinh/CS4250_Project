import sys
import scraper
import index_creator
import ranker

def main_menu():
    while True:
        print("\nSearch Engine Main Menu:")
        print("1. Start Web Scraper")
        print("2. View Indexed Documents")
        print("3. Search Documents")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # Start the web scraping process
            print("Starting Web Scraper...")
            start_scraping()
        elif choice == '2':
            # View Indexed Documents
            print("Viewing Indexed Documents...")
            create_inverted_index()
        elif choice == '3':
            # Search Documents
            query = input("Enter search query: ")
            search_documents(query)
        elif choice == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice, please enter a number between 1-4.")

def start_scraping():
    print("Web scraping started... ")

def create_inverted_index():
    print("Creating and displaying inverted index... ")

def search_documents(query):
    print(f"Searching for '{query}'... ")

if __name__ == "__main__":
    main_menu()
