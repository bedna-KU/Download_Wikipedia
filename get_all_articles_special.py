#!/usr/bin/env python3
import wikipediaapi
import os
import argparse
import re
import time
import requests
from bs4 import BeautifulSoup


########################################################
# PARAMETERS
########################################################

LANGUAGE = "sk"
BASE_URL = "https://" + LANGUAGE + ".wikipedia.org"
FIRST_PAGE = "/w/index.php?title=%C5%A0peci%C3%A1lne:V%C5%A1etkyStr%C3%A1nky&hideredirects=1"
DATA_DIR = "test"

########################################################

# Define terminal colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[36m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# If directory data do not exists create it
if not os.path.exists (DATA_DIR):
    os.makedirs (DATA_DIR)
if not os.path.exists ("errors"):
    os.makedirs ("errors")

wiki_html = wikipediaapi.Wikipedia (
        language = 'sk',
        extract_format = wikipediaapi.ExtractFormat.HTML
)

def scan_page (soup, counter):
    for link in soup.select ('ul.mw-allpages-chunk a[href]'):
        counter += 1
        page_name = link.text.replace (" ", "_")
        print (bcolors.BOLD + ">" + str (counter) + " " + page_name + bcolors.ENDC)
        with open (os.path.join (DATA_DIR, "list.txt"), "a") as text_file:
            text_file.write (page_name + "\n")
    return counter

if __name__ == "__main__":
    counter = 0
    current_page_href = FIRST_PAGE

    while current_page_href:
        response = requests.get (BASE_URL + current_page_href)
        soup = BeautifulSoup (response.content, "html.parser")
        counter = scan_page (soup, counter)
        current_page = soup.select ('div.mw-allpages-nav a[href]')
        current_page_href = current_page[1]["href"]
        print (bcolors.OKGREEN + ">>> " + current_page_href + bcolors.ENDC)
