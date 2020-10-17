#!/usr/bin/env python3
import wikipediaapi
import os
import argparse
import re
import time
from bs4 import BeautifulSoup


#########################################################
# PARAMETERS
#########################################################

LIST_FILE = "test/list.txt"    # List with articles
DATA_DIR = "test-articles"    # Directory for save files

#########################################################

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

def save_article (page_name, counter):
    page_content = wiki_html.page (page_name)
    soup = BeautifulSoup (page_content.text, "html.parser")
    only_p_tags = soup.find_all ('p')

    cleaned_text = ""
    for item in only_p_tags:
        if item.text:
            cleaned_text += item.text.strip () + "\n\n"
    # Strip beginning and trailing spaces
    cleaned_text = cleaned_text.strip ()
    # Remove lines shorten then 25 chars
    cleaned_text = re.sub (r'^.{0,25}$', '', cleaned_text, flags = re.MULTILINE)
    # Remove empty lines
    cleaned_text = re.sub (r'\n\s*\n', '\n\n', cleaned_text)
    # Rmove text under {}
    cleaned_text = re.sub (r'\{.*\}', '', cleaned_text)
    # For file save change dangerous slash to underscore
    if cleaned_text:
        counter += 1
        page_file_name = page_name.replace ("/", "_")
        print (bcolors.BOLD + "> " + str (counter) + " Save page: " + page_file_name + bcolors.ENDC)
        with open (os.path.join (DATA_DIR, page_file_name), "w") as text_file:
            text_file.write (cleaned_text)
    else:
        # For file save change dangerous slash to underscore
        page_file_name = page_name.replace ("/", "_")
        print (bcolors.WARNING + "> Error string is EMPTY:" + page_file_name + bcolors.ENDC)
        with open (os.path.join ("errors", "error_save_article.txt"), "a") as text_file:
            text_file.write (page_file_name + "\n")
    return counter

if __name__ == "__main__":
    counter = 0
    with open (os.path.join (LIST_FILE), "r") as text_file:
        for line in text_file:
            line = line.strip()
            print (line)
            counter = save_article (line, counter)
