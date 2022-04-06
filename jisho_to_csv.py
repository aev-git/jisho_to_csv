#this program takes a url to a specific word on www.jisho.org and
#exports that word, any furigana, and English definition to an excel
#spreadsheet that can be imported into Anki

import re
import csv
import traceback
from bs4 import BeautifulSoup
from urllib.request import urlopen

urls = []
vocabList = []

def process_tags(soup, cssSelector):
    tag = soup.select_one(cssSelector)
    
    if (tag is not None):
        word = ""
        for string in tag.stripped_strings:
            word += string
        print(word)
        return word

def process_definitions(soup, cssSelector):
    tag = soup.select_one(cssSelector)
    if (tag is not None):
        word = ""
        defs = tag.find_all(class_="meaning-meaning")
        for child in defs:
            line = str(child.string)
            if (line != "None"):
                word += ("\n" + line)  
        return word
            
def process_urls(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    expression = process_tags(soup, '.exact_block > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')
    reading = process_tags(soup, '.exact_block > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
    if (reading != ""):
        reading = "[" + reading + "]"
    
    vocabList.append([expression, expression + reading,
                     process_definitions(soup, '.exact_block > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)')])

if __name__ == "__main__":
    sourcefile = input("file to read from: ")
    exportfile = input("file to write to (must end in .csv):")

    try:
        #get urls from file
        print("reading urls...")
        f = open(sourcefile, "r")

        for x in f:
            urls.append(x)

        #get word info from webpage
        print("processing urls...")
        for url in urls:
            process_urls(url)
            
        #export data onto csv spreadsheet
        print("creating spreadsheet...")

        with open(exportfile, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(vocabList)

        print("finished!")
        f.close()
    except:
        print("An exception has occured")
        traceback.print_exc()
