# OTC---Search Engines

The tool we proposed is a vertical search engine that helps users finding the information about over-the-counter medicines online quickly. 
Users can type inthe name of the sickness/discomfort, the symptoms they experiencedor the name of over-the-counter medicines. 
The search engine will return the list of top 5 OTCs by ranks that are relevant to queries, as well as a link to a web page that provides more details. 

# List of Files

-flask_app.py is used for pythonanywhere.com to build the web-based search engine

-FindOTC_local.py is used to run the query in local bash terminal

-OTC_WebScraper.py is used to scrape data from www.drugs.com

-OTC_Data.csv is the output result file by running OTC_WebScraper.py

## Setup
We'll use [metapy](https://github.com/meta-toolkit/metapy)---Python bindings for MeTA. 
If you have not installed metapy so far, use the following commands to get started.

```bash
# Ensure your pip is up to date
pip install --upgrade pip

# install metapy!
pip install metapy 

# install pytoml
pip install pytoml

# install beautifulsoup4
pip install beautifulsoup4

```

download the chrome driver file to use "OTC_WebScraper.py" in the link below:
https://sites.google.com/a/chromium.org/chromedriver/downloads

Please note that different platforms and different google chrome versions require different drivers

If you're on an EWS machine
```bash
module load python3
# install metapy on your local directory
pip install metapy pytoml --user
```




