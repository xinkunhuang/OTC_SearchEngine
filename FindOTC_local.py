#Author: Xinkun Huang
#12/2/2019
#This is a version to run the query locally 


import sys
import time

import metapy
import pytoml



def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate, 
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    return metapy.index.OkapiBM25()


if __name__ == '__main__':

    cfg = "config.toml"
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)
        

    start_time = time.time()
    top_k = 5


    #Set query
    query = metapy.index.Document()

    print("Enter drug name or medical condition:")
    #get inputs from users
    from_user=input()
    #run one query and return top 5 OTCs
    query.content(from_user)
    
    results=[]

    #find the top 5 results
    results = ranker.score(idx, query, top_k)
    
    #print out the results
    for i in range(len(results)):
        doc_id_temp=results[i][0]
        with open('otc_names.txt') as f:
            name = f.read().splitlines()[doc_id_temp-1]
        with open('otc_urls.txt') as f:
            link = f.read().splitlines()[doc_id_temp-1]
        results.append((name,link))
    
    print()
    print("The top 5 results")
    for i in range(5):    
        print(results[i+5])
        print()
