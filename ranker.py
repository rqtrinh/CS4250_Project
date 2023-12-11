from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

''' 
Objectives: 
1.) Tokenize query
2.) Calculate tf-idf for query and vectorize it 
3.) Vectorize documents
4.) Cosine similarity between query and document vectors to obtain similarity rankings (first row)  
5.) Pagination (5 professors per page, non-zero degree of similarity) 
'''

# Document Vectors (variable)
#
# Format: 
#   - key -> faculty URL
#   - value -> array containing tf-idf vector for every indexed term
#
# Example:
# {
#   https://www.cpp.edu/faculty/alas : [term1_weight, term2_weight, term3_weight ... termn_weight] ,       
#   https://www.cpp.edu/faculty/parensburger/index.shtml: [term1_weight, term2_weight, term3_weight ... termn_weight],                                    
#   ...
# }

def rank_documents(query,db):
    
    # Initialization
    tfidf_index = list(db.tfidf_index.find())
    parsed_pages = list(db.parsed_pages.find())
    document_vectors = {}
    query_vector = [0] * len(tfidf_index)
    
    # Query Tokenization
    vectorizer = CountVectorizer(analyzer='word', stop_words='english')
    query_token_counts = vectorizer.fit_transform(query).toarray() # sparse matrix --> array
    query_tokens = vectorizer.vocabulary_
    
    # Initializing document_vectors 
    for page in parsed_pages:
        if page["_id"] not in document_vectors:
            document_vectors[page["_id"]] = [0] * len(tfidf_index)
    
    # Add weights from tfidf_index into the document vectors
    # If the index term is part of the query, calculate its tf-idf score and add it to the query vector
    for i, term in enumerate(tfidf_index):
        
        if term["_id"] in query_tokens:
            # tf-idf calculation
            tf = query_token_counts[0][query_tokens[term["_id"]]] / sum(query_token_counts[0])
            idf = math.log(len(tfidf_index) / len(term["weights"]))
            # add to query vector
            query_vector[i] = tf * idf
        
        # Add weights for the term in each document vector from tfidf index
        for doc, term_weight in term['weights'].items():
            document_vectors[doc][i] = term_weight
    
    # Compiling vectors 
    all_vectors = []
    all_vectors.append(query_vector)
    for vector in document_vectors.values(): 
        all_vectors.append(vector)
        
    # Cosine Similarity 
    similarity_matrix = cosine_similarity(all_vectors)
    rankings = similarity_matrix[0][1:len(similarity_matrix[0])] # remove 1st element 
    print(rankings)
    
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

# test_query = ["The dogs slept behind the churches."]
query = [input("Enter a query: ")]
db = connectDatabase()
rank_documents(query,db)