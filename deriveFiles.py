#!/usr/bin/python

"""Split up master list of paper titles, authors, and sessions
(completePaperList.csv) into the various files needed by Meinard's
scripts for generating the pdf proceedings (papers.tex) and the
electronic proceedings.

"""

import csv
import codecs
import io

def unicode_csv_reader(utf8_data, dialect="excel", **kwargs):
    """This function will read a csv file and will interpret the
    contained data as utf-8.

    """
    #csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    csv_reader = csv.reader(utf8_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def unicode_tsv_reader(utf8file):
    "Generator for reading a tab-delimited file"
    for line in utf8file.readlines():
        #yield [cell for cell in unicode(line, 'utf-8').rstrip('\n\r').split('\t')]
        yield [cell for cell in line.rstrip('\n\r').split('\t')]
        
def generatePapersDotTex(csvFile):
    lastSession = ""
    sessionInfo = loadSessionInfo()
    # with io.open('2016_Proceedings_ISMIR/papers.tex', 'w', encoding='utf-8') as papersDotTex:
    # with codecs.open('2016_Proceedings_ISMIR/papers.tex', 'w', 'utf-8') as papersDotTex:
    with open('2016_Proceedings_ISMIR/papers.tex', 'w') as papersDotTex:
        for title, authors, number, session in unicode_tsv_reader(csvFile):
            if session != lastSession:
                name, page = sessionInfo[session]
                papersDotTex.write(papersSectionHeader(name, page))
            lastSession = session
            
            papersDotTex.write('\includepaper{%s}{%s}{articles/%03d_Paper}\n'
                               % (title, authors, int(number)))


def papersSectionHeader(name, page):
    chunk = """

\\thispagestyle{empty}\\cleardoublepage
\\addcontentsline{toc}{section}{%s}
\\includepdf[pages=%s,pagecommand=\\thispagestyle{empty}]{external/12_Sessions.pdf}%%
\\thispagestyle{empty}\\cleardoublepage

""" % (name, page)
    return chunk

def loadSessionInfo():
    with open('data/sessionInfo.csv') as csvFile:
        return {k: (name, int(num)) for k, name, num in unicode_tsv_reader(csvFile)}

def generateElectronicCsvFiles(csvFile):
    pass


def main():
    with open('data/completePaperList.csv') as csvFile:
        generatePapersDotTex(csvFile)
        generateElectronicCsvFiles(csvFile)



if __name__ == '__main__':
    main()
    
