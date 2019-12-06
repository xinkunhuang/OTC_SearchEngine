from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import urllib
import pandas as pd
import csv
import re
import os
import pathlib as path
import logging
import threading
import time
import sys
import numpy as np

# Initializing browser object which is invoked to call load page in chrome headless mode.
options = Options()
options.headless = True
browser = webdriver.Chrome('chromedriver.exe', options=options)


# Function to read the url and load the content as BeautifulSoup
def get_js_soup(url, browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
    return soup


# Below Function will return list of URL link to scrape from drugs.com
# The links can be traversed alphabatically  like https://www.drugs.com/alpha/ab.html , https://www.drugs.com/alpha/ac.html
# Each Link will refer to page which further contains all the Medication. For example
# https://www.drugs.com/alpha/ab.html is link which contain all the Medication link which start with letter "ab"
def create_urls_to_scrape():
    links = []
    baseUrl = 'https://www.drugs.com/alpha/'
    hyperLink = ''
    alphabet_count = 26
    alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', '0-9']
    aplhabet_hyperlink_count = 27
    for c1 in range(alphabet_count - 1):
        for c2 in range(aplhabet_hyperlink_count):
            links.append(baseUrl + alphabet_list[c1] + alphabet_list[c2] + ".html")

    # print(links)
    return links


# Below will go over the links which has been found from function  "create_urls_to_scrape"
# It will go to each of link and then fetch all the Medication Links from that page and store in the file.
# For Example,if Link https://www.drugs.com/alpha/ab.html contain two medication link m1.html and m2.html
# Code will fetch both this link and store it in file named "Medication_Links.csv
# ------------------------------------------------------------------------------------------------------------
# Params:
# links_to_browse : links which has been found from function  "create_urls_to_scrape" to be used to go over Medication
# Links
# ------------------------------------------------------------------------------------------------------------
def get_all_medication_links(links_to_browse):
    medication_links = []
    count = 0
    file_medication_links = open('Medication_Links.csv', 'w')

    for link_count in range(len(links_to_browse)):
        soup = get_js_soup(links_to_browse[link_count], browser)
        try:
            for link_holder in soup.find_all('ul', class_='ddc-list-column-2'):
                li_list = link_holder.find_all('li')  # get ur
                for li in li_list:
                    if li.find('a') is not None:
                        link = li.find('a')['href']
                        medication_links.append('https://www.drugs.com/' + link)
                        file_medication_links.write('https://www.drugs.com/' + link)
                        file_medication_links.write('\n')
                        count = count + 1
                        print(count)
        except:
            print('adadad')
    file_medication_links.close()
    # return medication_links


# Below function will go to each Medication Page(URL) and retrieve the relevant information
# After having 100 Medication Link scrapped and content stored in pandas dataframe, it will save all the content
# from dataframe into "VerticalSearchEngine_Final.csv". This will help in recovery in case system crash or code
# crashed or timeout.System when booted can continue from where it left the file.
# ------------------------------------------------------------------------------------------------------------
# Params:
# url_path :URL Path of Medication to scrape
# browser : Chrome browser object
# pd_df_VSearchEngine : pandas dataframe to store relevant information
# row_count: row index inside dataframe where information is stored
# file_name: Name of file storing Information for scrapped content It is just another reflection of the DataFrame)
# ------------------------------------------------------------------------------------------------------------

def browse_medication_page_n_store_meta_data(url_path, browser, pd_df_VSearchEngine, row_count, file_name):
    try:
        # Below will scrape the relevant content from Medication URL
        soup = get_js_soup(url_path, browser)
        text = ''
        pattern = re.compile('What is*')
        link_holders = soup.findAll('h2', text=pattern)

        if len(link_holders) == 0:
            pattern = re.compile('Uses for*')
            link_holders = soup.findAll('h2', text=pattern)

        if len(link_holders) > 0:
            # for link_holder in soup.find_all('div',class_='contentAd contentAdM1 contentAdAlone'):
            for link_holder in link_holders:
                next_td_tag = link_holder.findNext('p')
                text = text + next_td_tag.get_text()
                keep_going = True
                next_td_tag = next_td_tag.find_next_sibling()
                # print(next_td_tag)

                while keep_going == True:
                    # print(next_td_tag)
                    if next_td_tag.name == 'p':
                        text = text + next_td_tag.get_text()
                        next_td_tag = next_td_tag.find_next_sibling()

                    elif next_td_tag.name is not 'p':
                        keep_going = False

        status = soup.find_all("div", class_=lambda value: value and value.startswith("ddc-status-icon drugInfoRx"))
        medicine_name = soup.find_all('div', class_='contentBox')

        if len(status) == 0:
            status = 'No Information'
        else:
            status = status[0].get_text()

        if len(medicine_name) == 0:
            medicine_name = 'No Information'
        else:
            medicine_name = medicine_name[0].find_next('h1').get_text()

        # Store the Relevant Information into Pandas Dataframe
        pd_df_VSearchEngine.iloc[row_count, 0] = medicine_name
        pd_df_VSearchEngine.iloc[row_count, 1] = url
        pd_df_VSearchEngine.iloc[row_count, 2] = status
        pd_df_VSearchEngine.iloc[row_count, 3] = text

        print("####" + str(row_count))
        if (row_count - int(start_index)) % 100 == 0:
            pd_df_VSearchEngine.to_csv(file_name, index=False)
    except:
        # In case some error occur , store the content as No Information so that User can get idea which Medication link
        # Cann't be scrapped
        pd_df_VSearchEngine.iloc[row_count, 0] = "No Information"
        pd_df_VSearchEngine.iloc[row_count, 2] = "No Information"
        pd_df_VSearchEngine.iloc[row_count, 3] = "No Information"

        print("####" + str(row_count))
        if (row_count - int(start_index)) % 100 == 0:
            pd_df_VSearchEngine.to_csv(file_name, index=False)


# Belwo will read the Medication_Links.csv and load all the content into Padas Dataframe
def read_medicaton_links_csv():
    try:
        df = pd.read_csv('Medication_Links.csv', header=None, delim_whitespace=True)
    except:
        return None
    return df


# calling function to return the url link to browse alphabetically
links_to_browse = create_urls_to_scrape()
# Calling function to return all the Medication Links to Scrape
df_medication_links = read_medicaton_links_csv()

# If there is already Medication_Links.csv , No need to scrape it again
# This is necessary in case during crawling system crashed or code crashed.
if df_medication_links is None:
    get_all_medication_links(links_to_browse)
    df_medication_links = read_medicaton_links_csv()

# Initialing Start and End Index which is number of Medication Links to Scrape
# After
start_index = '0'
end_index = df_medication_links.shape[0]
verticalengine_metadata_file = "VerticalSearchEngine_Final.csv"

# Check if there exist already "Vertical_Engine_MetaDataFile
# If yes ,read the content into pandas dataframe
# If nom ,create new panda dataframe with column name and init the URL Field
if os.path.exists(verticalengine_metadata_file):
    pd_df_VSearchEngine = pd.read_csv(verticalengine_metadata_file)
else:
    pd_df_VSearchEngine = pd.DataFrame(columns=['Medication Name', 'URL', 'Pres Type', 'Information', 'Full Content'])
    pd_df_VSearchEngine['URL'] = df_medication_links[0]

# Loop over each row of Dataframe and read the column name "URL" which is url of Medication to scrape,
# Call "function browse_medication_page_n_store_meta_data" and store the result of scrapped data into row which
# can be identified using "row_count". Below will also check if the first column ("'Medication Name'") of the row
# is empty or not. If Empty means the  Medication Link(identified by "URL" Column ) is not being scrapped ,
# So need to call "function browse_medication_page_n_store_meta_data" otherwise just skip
for row_count in range(int(start_index), int(end_index)):
    url = pd_df_VSearchEngine.iloc[row_count, 1]
    if pd.isnull(pd_df_VSearchEngine.iloc[row_count, 0]):
        browse_medication_page_n_store_meta_data(url, browser, pd_df_VSearchEngine, row_count,
                                                 verticalengine_metadata_file)
        print(row_count)

# Store the pandas dataframe into ""VerticalSearchEngine_Final.csv"
pd_df_VSearchEngine.to_csv(verticalengine_metadata_file, index=False)
