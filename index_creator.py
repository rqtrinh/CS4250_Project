from collections import defaultdict
import math
from pymongo import MongoClient


#tokenized_docs is a list of objects of this following format

#{
#   _id: string (document url),
#   words: dict; {word: term freq in document}
# }
#


#invert into dict
    #key: token
    #value: dict where key = doc id and value = token freq
def create_inverted_index(tokenized_docs):
    #dict of inverted indexes
    inverted_index = defaultdict(dict)

#for each document and its corresponding dict of token freqs
    for doc_obj in tokenized_docs:
        #extract doc id and token freq dict
        doc_id, token_freq_dict = doc_obj.values()

        #iterate through each token in token freqs
        for token, token_freq in token_freq_dict.items():

            #if token is not in the index yet, initialize its dict
            if token not in inverted_index:
                inverted_index[token] = {}
            
            #then store the token freq in the doc dict
            inverted_index[token][doc_id] = token_freq
    return inverted_index


#tf = count of current token / total number of tokens in document
#given tokenized_docs, will compute tf for token in doc
#returns dict where 
#   key = token, 
#   value = dict where 
#       key = doc_id
#       val = tf for current token in this document

def compute_tf(tokenized_docs):
    tf_dict = {}
    for doc_obj in tokenized_docs:
        #extract doc id and token freq dict
        doc_id, token_freq_dict = doc_obj.values()

        #get total token count in current doc
        curr_doc_token_count = 0
        for token_count in token_freq_dict.values():
            curr_doc_token_count+=token_count

        #iterate through each token in token freqs
        for token, token_freq in token_freq_dict.items():
            #if the token is not in tf dict yet, init dict for it
            if token not in tf_dict:
                tf_dict[token] = {}

            #calc tf for current token, store key as doc_id and val as tf
            tf_dict[token][doc_id] = token_freq / curr_doc_token_count

    return tf_dict
        
        

    
#computes tfidf
#tfidf = tf * idf

def compute_tfidf(inverted_index, tokenized_docs):
    #get number of total docs
    N = len(tokenized_docs)

    #dict to store tfidf
    tfidf_index = defaultdict(dict)

    #get tf for all tokens in corresponding docs
    tf_index = compute_tf(tokenized_docs)

    for token, doc_list in inverted_index.items():
        #idf = log( total num docs / number of docs with current token)
        idf = math.log(N / len(doc_list))

        #get tf for current token in this doc
        tf = tf_index[token]
        #for each doc id for this token
        for doc_id in doc_list.keys():
            #get tf for current token in current doc
            tf = tf_index[token][doc_id]
            tfidf = tf * idf
            tfidf_index[token][doc_id] = tfidf
    return tfidf_index


#stores weights for each term in document
def store_tfidf_index(tfidf_index, db):
    #for each term and its weights for all docs
    for term, doc_weights in tfidf_index.items():

        #see if there is already recorded weights for this term, if so update, otherwise insert
        try:
            term_weights = db.tfidf_index.find_one({'_id': term})
            if(term_weights):
                db.tfidf_index.update_one({'_id': term}, {"$set": {'weights': doc_weights}})
            else:
                db.tfidf_index.update_one({'_id': term, 'weights': doc_weights})
        except:
            print("error inserting tfidf weights")


#connects to db
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


db = connectDatabase()
parsed_pages = list(db.parsed_pages.find())
inverted_page_index = create_inverted_index(parsed_pages)

tfidf_index_dict = compute_tfidf(inverted_index=inverted_page_index, tokenized_docs=parsed_pages)



