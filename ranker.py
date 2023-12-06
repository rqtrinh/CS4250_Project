from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import pandas as pd

# Resources: 
# - https://www.geeksforgeeks.org/web-information-retrieval-vector-space-model/  
# - https://www.cl.cam.ac.uk/teaching/1415/InfoRtrv/lecture4.pdf 
# - https://spotintelligence.com/2023/09/07/vector-space-model/ 

''' 
Objectives: 
1.) Tokenize query
2.) Calculate tf-idf scores for each token
    - Only consider already indexed terms (any term that exists in the index)
    - for tf use query, for idf use previously calculated idf 
3.) Vectorize documents
4.) Cosine similarity between query and document vectors to obtain similarity rankings (first row )  
5.) Pagination (5 professors per page, non-zero degree of similarity) 
'''

# X = [0.57735027, 0.57735027, 0.57735027]
# Y = [1, 1, 0.8]
# print(cosine_similarity([X,Y]))

# print(vectorizer.vocabulary_)
# print(query_vector.shape)
# print(query_vector.toarray())
# print(pd.DataFrame(data = query_vector.toarray(),index = ['query'],columns = token_names))

def rank_documents(query,tfidf_index):
    
    vectorize_query(query,tfidf_index)
    
    
def vectorize_query(query,tfidf_index):
    vectorizer = CountVectorizer(analyzer='word', stop_words='english')
    vectorizer.fit(query)
    tfidf_vectorizer = TfidfVectorizer(analyzer='word',stop_words='english')
    query_vector = tfidf_vectorizer.fit_transform(query)
    token_names = tfidf_vectorizer.get_feature_names_out()
    
    # df = pd.DataFrame(data = query_vector.toarray(), index = ['query'], columns = token_names)
    # for term in df:
    #     if term in tfidf_index:
    #         df.drop(term,axis=1)
        
            
    # return query_vector

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


test_query = ["The dogs slept behind the churches."]
db = connectDatabase()
terms = list(db.tfidf_index.find())
rank_documents(test_query)