import codecs
import csv
import os

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
# This function will read a csv file and will interpret
# the contained data as utf-8.
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def search_pages_total(paper_name, pages_total):
    for current_row in pages_total: #go through the rows in pages_total
        current_row = str(current_row[0]).split(',')  #split row after comma
        current_paper_name = current_row[0] #paper_name = first "cell"
        current_pages = int(current_row[1]) # number of pages  = second "cell"
        if paper_name in current_paper_name: # if paper name matches the name in the list of papers
            return current_pages
    raise BaseException("Paper not found: %s" % paper_name)
        
def makeDirs(path):
    sub_path = os.path.dirname(path)
    if sub_path == path:
        raise "sub_path == path: %s" % path
    if len(sub_path) > 0 and not os.path.exists(sub_path):
        makeDirs(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

