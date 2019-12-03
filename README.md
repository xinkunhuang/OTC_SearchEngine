# OTC---Search Engines

The tool we proposed is a vertical search engine that helps users finding the information about over-the-counter medicines online quickly. 
Users can type inthe name of the sickness/discomfort, the symptoms they experiencedor the name of over-the-counter medicines. 
The search engine will return the list of top 5 OTCs by ranks that are relevant to queries, as well as a link to a web page that provides more details. 

# Applications

-flask_app.py is used for pythonanywhere.com to build the web-based search engine
-FindOTC_local.py is used to run the query in local bash terminal

## Setup
We'll use [metapy](https://github.com/meta-toolkit/metapy)---Python bindings for MeTA. 
If you have not installed metapy so far, use the following commands to get started.

```bash
# Ensure your pip is up to date
pip install --upgrade pip

# install metapy!
pip install metapy pytoml
```

If you're on an EWS machine
```bash
module load python3
# install metapy on your local directory
pip install metapy pytoml --user
```



## Indexing the data
To index the data using metapy, you can use either Python 2 or 3.
```python
import metapy
idx = metapy.index.make_inverted_index('config.toml')
```

## Search the index
You can examine the data inside the cranfield directory to get a sense about the dataset and the queries.

To examine the index we built from the previous section. You can use metapy's functions.

```python
# Examine number of documents
idx.num_docs()
# Number of unique terms in the dataset
idx.unique_terms()
# The average document length
idx.avg_doc_length()
# The total number of terms
idx.total_corpus_terms()
```

Here is a list of all the rankers in MeTA.Viewing the class comment in the header files shows the optional parameters you can set in the config file:

- [Okapi BM25](https://github.com/meta-toolkit/meta/blob/master/include/meta/index/ranker/okapi_bm25.h), method = "**bm25**" 
- [Pivoted Length Normalization](https://github.com/meta-toolkit/meta/blob/master/include/meta/index/ranker/pivoted_length.h), method = "**pivoted-length**"
- [Absolute Discount Smoothing](https://github.com/meta-toolkit/meta/blob/master/include/meta/index/ranker/absolute_discount.h), method = "**absolute-discount**"
- [Jelinek-Mercer Smoothing](https://github.com/meta-toolkit/meta/blob/master/include/meta/index/ranker/jelinek_mercer.h), method = "**jelinek-mercer**"
- [Dirichlet Prior Smoothing](https://github.com/meta-toolkit/meta/blob/master/include/meta/index/ranker/dirichlet_prior.h), method = "**dirichlet-prior**"

In metapy, the rankers can be called as:

```python
metapy.index.OkapiBM25(k1, b, k3) where k1, b, k3 are function arguments, e.g. ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)
metapy.index.PivotedLength(s) 
metapy.index.AbsoluteDiscount(delta)
metapy.index.JelinekMercer(lambda)
metapy.index.DirichletPrior(mu)
```

## Varying a parameter
Choose one of the above retrieval functions and one of its parameters (don’t choose BM25 + k3, it’s not interesting). For example, you could choose Dirichlet Prior and mu.

Change the **ranker** to your method and parameters. In the example, it is set to **bm25**. Use at least 10 different values for the parameter you chose; try to choose the values such that you can find a maximum MAP.

Here's a tutorial on how to do an evaluation of your parameter setting (this code is included in *search_eval.py*):


```python
# Build the query object and initialize a ranker
query = metapy.index.Document()
ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)
# To do an IR evaluation, we need to use the queries file and relevance judgements.
ev = metapy.index.IREval('config.toml')
# Load the query_start from config.toml or default to zero if not found
with open('config.toml', 'r') as fin:
        cfg_d = pytoml.load(fin)
query_cfg = cfg_d['query-runner']
query_start = query_cfg.get('query-id-start', 0)
# We will loop over the queries file and add each result to the IREval object ev.
num_results = 10
with open('cranfield-queries.txt') as query_file:
    for query_num, line in enumerate(query_file):
        query.content(line.strip())
        results = ranker.score(idx, query, num_results)                            
        avg_p = ev.avg_p(results, query_start + query_num, num_results)
        print("Query {} average precision: {}".format(query_num + 1, avg_p))
ev.map()
```

## Writing InL2

You will now implement a retrieval function called InL2. It is described in [this](http://dl.acm.org/citation.cfm?id=582416) paper: 
For this assignment, we will only concern ourselves with writing the function and not worry about its derivation. 
InL2 is formulated as $`Score(Q,D) = \sum_{t\in Q\cap D} c(t,Q)\cdot \frac{tfn}{tfn+c}\cdot\log_2(\frac{N+1}{c(t,C)+0.5})`$
where $`tfn = c(t,D) \cdot \log_2\left(1+\frac{avgdl}{|D|}\right)`$

It uses the following variables:

- $`Q,D,t`$ : the current query, document, and term
- $`N`$: the total number of documents in the corpus C
- $`avgdl`$: the average document length
- $`c > 0`$: is a parameter

Determine if this function captures the TF, IDF, and document length normalization properties. Where (if anywhere) are they represented in the formula? You don’t need to submit your answers.

To implement InL2, define your own ranking function in Python, as shown below. 
You do not need to create a new file, the template is included in *search_eval.py*  You will need to modify the function **score_one**. 
Do not forget to call the InL2 ranker by editing the return statement of *load_ranker* function inside search_eval.py.

The parameter to the function is a score_data sd object. See the object [here](https://github.com/meta-toolkit/meta/blob/master/include/meta/index/score_data.h).

As you can see, the sd variable contains all the information you need to write the scoring function. The function you’re writing represents one term in the large InL2 sum.

```python
class InL2Ranker(metapy.index.RankingFunction):                                            
    """                                                                          
    Create a new ranking function in Python that can be used in MeTA.             
    """                                                                          
    def __init__(self, some_param=1.0):                                             
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()                                        
                                                                                 
    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
        return (self.param + sd.doc_term_count) / (self.param * sd.doc_unique_terms + sd.doc_size)
```


## Varying InL2’s parameter
Perform the same parameter analysis with InPL2’s $`c`$ parameter. 
