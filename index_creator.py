from collections import defaultdict
import math

def create_inverted_index(tokenized_docs):
    inverted_index = defaultdict(dict)

    for doc_id, tokens in tokenized_docs.items():
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        for term, freq in term_freq.items():
            if term not in inverted_index:
                inverted_index[term] = {}
            inverted_index[term][doc_id] = freq

    return inverted_index

def compute_tfidf(inverted_index, tokenized_docs):
    N = len(tokenized_docs)
    tfidf_index = defaultdict(dict)

    for term, doc_list in inverted_index.items():
        idf = math.log(N / len(doc_list))
        for doc_id, tf in doc_list.items():
            tfidf = tf * idf
            tfidf_index[term][doc_id] = tfidf

    return tfidf_index

def store_tfidf_index(tfidf_index, db):
    for term, doc_weights in tfidf_index.items():
        db.tfidf_index.insert_one({'term': term, 'weights': doc_weights})