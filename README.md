# OTC---Search Engines

The tool we proposed is a vertical search engine that helps users finding the information about over-the-counter medicines online quickly. 
Users can type inthe name of the sickness/discomfort, the symptoms they experiencedor the name of over-the-counter medicines. 
The search engine will return the list of top 5 OTCs by ranks that are relevant to queries, as well as a link to a web page that provides more details. 

# List of Files

-"flask_app.py" is used for pythonanywhere.com to build the web-based search engine

-"FindOTC_local.py" is used to run the query in local bash terminal

-"OTC_WebScraper.py" is used to scrape data from www.drugs.com

-"OutputfromWebScraper.csv" is the output result file by running OTC_WebScraper.py. There are 18874 data entries(drugs) extracted. We filtered the data to only have OTC and OTC/RX drugs. The filtered dataset has 3673 entries. There are four columns: 1. Medication Name	2. URL 3.Pres Type(drug type) 4.Information Full Content, which is a short description paragraph on the drug.

-"cranfield/cranfield.dat" is the "information full content" column data from "OutputfromWebScraper.csv".

-"otc_names.txt" is the "Medicate Name" column data from "OutputfromWebScraper.csv".

-"otc_urls.txt" is the "Medicate Link" column data from "OutputfromWebScraper.csv".

-"cranfield/line.toml" tells metapy that each document is separated by line for corpus.

-"stopwords.txt" contains list of commond words, like "the" and "a".

-"chromedriver.exe" is used to scrape the data from www.drugs.com. Please note that different platforms and different google chrome versions require different drivers. download the chrome driver file to use "OTC_WebScraper.py" in the link:
https://sites.google.com/a/chromium.org/chromedriver/downloads

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



If you're on an EWS machine
```bash
module load python3
# install metapy on your local directory
pip install metapy pytoml beautifulsoup4 --user
```




