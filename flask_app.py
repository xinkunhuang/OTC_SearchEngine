
import math
import sys
import time
import os

import metapy
import pytoml

from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "fdafagagrfrrcbklpiaonwehycbkjdksjdka"


'''
This is the main function for flask to build the page
'''
@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
    
    userinput = None
    userinput = request.form["userinput"]


        if userinput is not None:
            result = search(userinput)


            return '''
                <html>
                    <body>
                        <table style="width:100%">
                            <caption><h1>Top 5 Results</h1></caption>
                                <tr style="text-align:center;">
                                    <th>OTC Name</th>
                                    <th>Link</th>
                                </tr>
                                 <tr style="text-align:center;">
                                    <td>{result[0]}</td>
                                    <td>
                                        <a href={result[1]}>{result[1]}</a>
                                    </td>
                                 </tr>
                                 <tr style="text-align:center;">
                                    <td>{result[2]}</td>
                                    <td>
                                        <a href={result[3]}>{result[3]}</a>
                                    </td>
                                 </tr>
                                 <tr style="text-align:center;">
                                    <td>{result[4]}</td>
                                    <td>
                                        <a href={result[5]}>{result[5]}</a>
                                    </td>
                                 </tr>
                                 <tr style="text-align:center;">
                                    <td>{result[6]}</td>
                                    <td>
                                        <a href={result[7]}>{result[7]}</a>
                                    </td>
                                 </tr>
                                 <tr style="text-align:center;">
                                    <td>{result[8]}</td>
                                    <td>
                                        <a href={result[9]}>{result[9]}</a>
                                    </td>
                                 </tr>
                        </table>
                        <p><a href="/">Click here to search again</a>
                    </body>
                </html>
            '''.format(result=result)
    return '''
        <html>
            <body>
                {errors}
                <center><img src="/static/drugs_logo.jpg" alt="logo" width="300" height="200"></center>
                <h1 style="text-align:center;">Find your OTC:</h1>
                <form method="post" action=".">
                    <p style="text-align:center;"><input name="userinput"  placeholder="Enter drug name or medical condition" size="50"/></p>
                    <p style="text-align:center;"><input type="submit" value="Search" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

'''
This function will takes a string argument and return a list of top 5 results 
[names[0],links[0],names[1],links[1],names[2],links[2],names[3],links[3],names[4],links[4]]
'''
def search(userinput):
    top_k=5

    #Load settings from config.toml
    cfg = os.path.abspath("config.toml")


    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)


    #run one query and return top 5 OTCs
    query = metapy.index.Document()
    query.content(userinput)

    results = ranker.score(idx, query, top_k)

    links=[]
    names=[]

    for i in range(len(results)):
        doc_id_temp=results[i][0]
        with open(os.path.abspath("otc_urls.txt")) as f:
            links.append(f.read().splitlines()[doc_id_temp])
        with open(os.path.abspath("otc_names.txt")) as f:
            names.append(f.read().splitlines()[doc_id_temp])


    try:
        return [names[0],links[0],names[1],links[1],names[2],links[2],names[3],links[3],names[4],links[4]]
    except:
        return ["No result","","","","","","","","",""]

def load_ranker(cfg_file):
    #use BM25 method
    return metapy.index.OkapiBM25()

