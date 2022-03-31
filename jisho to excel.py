#this program takes a url to a specific word on www.jisho.org and
#exports that word, any furigana, and English definition to an excel
#spreadsheet that can be imported into Anki

import re
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
from openpyxl import Workbook

kanjiList = []
furiganaList = []
definitionList = []
urls = []
    
def write_to_spreadsheet(workbook, data, col):
    sheet = workbook.active
    for i in range(0, len(data)):
        cellref = sheet.cell(row=i+1, column=col)
        cellref.value = data[i];
        
def create_vocab_spreadsheet(path):
    workbook = Workbook()
    write_to_spreadsheet(workbook, kanjiList, 1)
    write_to_spreadsheet(workbook, furiganaList, 2)
    write_to_spreadsheet(workbook, definitionList, 3)
    workbook.save(path)

def process_tags(soup, cssSelector, targetList):
    tag = soup.select_one(cssSelector)
    
    if (tag is not None):
        word = ""
        for string in tag.stripped_strings:
            word += string
        print("data: " + word)
        targetList.append(word)

def process_definitions(soup, cssSelector, targetList):
    tag = soup.select_one(cssSelector)
    if (tag is not None):
        word = ""
        defs = tag.find_all(class_="meaning-meaning")
        for child in defs:
            line = str(child.string)
            if (line != None):
                word += ("\n" + line)
            
        print("data: " + word)
        targetList.append(word)
            
def process_urls(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    print("processing kanji...")
    process_tags(soup, '.exact_block > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)', kanjiList)

    print("processing furigana...")
    process_tags(soup, '.exact_block > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)', furiganaList)

    print("processing definitions...")
    process_definitions(soup, '.exact_block > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)', definitionList)

if __name__ == "__main__":
    sourcefile = input("file to read from: ")
    exportfile = input("file to write to (must end in .xlsx):")
    
    #get urls from file
    print("reading urls...")
    f = open(sourcefile, "r")

    for x in f:
        urls.append(x)

    #get word info from webpage
    print("processing urls...")
    for url in urls:
        process_urls(url)
        
    #export data onto spreadsheet
    print("creating spreadsheet...")
    create_vocab_spreadsheet(exportfile)
    print("finished!")
    f.close()
