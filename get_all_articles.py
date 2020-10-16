import wikipediaapi
import os
import argparse
import re
import time
from bs4 import BeautifulSoup


####################################################
# PARAMETERS
####################################################

DATA_DIR = "list"    # Directory for articles
LANGUAGE = "sk"      # Set lang

####################################################

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
if not os.path.exists ("error_list"):
    os.makedirs ("error_list")

# Set download type as HTML
wiki_html = wikipediaapi.Wikipedia (
        language = LANGUAGE,
        extract_format = wikipediaapi.ExtractFormat.HTML
)

main_categories = ["Príroda",
                    "Spoločnosť",
                    "Prírodné vedy",
                    "Spoločenské, humanitné a aplikované vedy",
                    "Technika",
                    "Umenie"]

def scan_categories (categorymembers, counter, level = 0, max_level = 100):
    for c in categorymembers.values ():
        print ("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == 0:
            if c.title:
                counter += 1
                # Replace space with underscore
                page_file_name = c.title.replace (" ", "_")
                print (bcolors.BOLD + ">" + str (counter) + " " + page_file_name + bcolors.ENDC)
                with open (os.path.join (DATA_DIR, "list.txt"), "a") as text_file:
                    text_file.write (page_file_name + "\n")
            else:
                # Replace space with underscore
                page_file_name = c.title.replace (" ", "_")
                print (bcolors.WARNING + "> Error string is EMPTY:" + page_file_name + bcolors.ENDC)
                with open (os.path.join ("error_list", "list.txt"), "a") as text_file:
                    text_file.write (page_file_name + "\n")
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            counter = scan_categories (c.categorymembers, counter, level = level + 1, max_level = max_level)
    return counter

if __name__ == "__main__":
    counter = 0
    for category in main_categories:
        cat = wiki_html.page ("Category:" + category)
        counter = scan_categories (cat.categorymembers, counter)
