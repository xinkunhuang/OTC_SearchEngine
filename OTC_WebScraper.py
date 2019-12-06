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

options = Options()
options.headless = True
browser = webdriver.Chrome('chromedriver.exe', options=options)


def get_js_soup(url, browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
    return soup


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


def browse_medication_page_n_store_meta_data(url_path, browser, pd_df_VSearchEngine, row_count, start_index, end_index):
    try:
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

        pd_df_VSearchEngine.iloc[row_count, 0] = medicine_name
        pd_df_VSearchEngine.iloc[row_count, 1] = url
        pd_df_VSearchEngine.iloc[row_count, 2] = status
        pd_df_VSearchEngine.iloc[row_count, 3] = text

        print("####" + str(row_count))
        if (row_count - int(start_index)) % 100 == 0:
            print("Inside")
            fileName = (start_index) + "_" + (end_index) + ".csv"
            print(fileName)
            pd_df_VSearchEngine.to_csv(fileName, index=False)
    except:
        pd_df_VSearchEngine.iloc[row_count, 0] = "No Information"
        pd_df_VSearchEngine.iloc[row_count, 2] = "No Information"
        pd_df_VSearchEngine.iloc[row_count, 3] = "No Information"

        print("####" + str(row_count))
        if (row_count - int(start_index)) % 100 == 0:
            print("Inside")
            fileName = (start_index) + "_" + (end_index) + ".csv"
            print(fileName)
            pd_df_VSearchEngine.to_csv(fileName, index=False)


def read_medicaton_links_csv():
    try:
        df = pd.read_csv('Medication_Links.csv', header=None, delim_whitespace=True)
    except:
        return None
    return df


#start_index = sys.argv[1]
#end_index = sys.argv[2]
start_index = '20000'
end_index = '30000'
fileName = (start_index) + "_" + (end_index) + ".csv"

links_to_browse = create_urls_to_scrape()
df_medication_links = read_medicaton_links_csv()
if df_medication_links is None:
    get_all_medication_links(links_to_browse)
    df_medication_links = read_medicaton_links_csv()

if os.path.exists(fileName):
    pd_df_VSearchEngine = pd.read_csv(fileName)
else:
    pd_df_VSearchEngine = pd.DataFrame(columns=['Medication Name', 'URL', 'Pres Type', 'Information', 'Full Content'])
    pd_df_VSearchEngine['URL'] = df_medication_links[0]

print("start_index: " + (start_index) + " end_index: " + (end_index))
for row_count in range(int(start_index), int(end_index)):
    url = pd_df_VSearchEngine.iloc[row_count, 1]
    if pd.isnull(pd_df_VSearchEngine.iloc[row_count, 0]):
        browse_medication_page_n_store_meta_data(url, browser, pd_df_VSearchEngine, row_count, start_index, end_index)
        print(row_count)

pd_df_VSearchEngine.to_csv(fileName, index=False)
