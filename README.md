# Download_Wikipedia
Download all articles from Wikipedia by language

## Change language
Change `LANGUAGE = "sk"` `in get_all_articles.py` into any language.

Change `main_categories` to categories from main page Wikipedia by language

## Download all articles names

Get all articles from categories

`get_all_articles.py`

Extract only unique articles `awk '!seen[$0]++' list/list1.txt > list/list-uniq.txt`

## Download all articles names from special

Better results with 'Special:AllPages'

`get_all_articles_special.py`

For other languages, you must also change Slovak "Ďalšie" by language

## Download text from all pages

download.py
