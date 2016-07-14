#!/usr/bin/python

"""Split up master list of paper titles, authors, and sessions
(completePaperList.csv) into the various files needed by Meinard's
scripts for generating the pdf proceedings (papers.tex) and the
electronic proceedings.

"""

import csv
import collections
import os
import shutil

def unicode_csv_reader(utf8_data, dialect="excel", **kwargs):
    """This function will read a csv file and will interpret the
    contained data as utf-8.

    """
    #csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    csv_reader = csv.reader(utf8_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def unicode_tsv_reader(utf8FileName):
    "Generator for reading a tab-delimited file"
    with open(utf8FileName) as utf8file:
        for line in utf8file.readlines():
            #yield [cell for cell in unicode(line, 'utf-8').rstrip('\n\r').split('\t')]
            yield [cell for cell in line.rstrip('\n\r').split('\t')]
        
def generatePapersDotTex(csvFile):
    lastSession = ""
    sessionInfo = loadSessionInfo()
    authorCount = collections.defaultdict(int)
    
    # with io.open('2016_Proceedings_ISMIR/papers.tex', 'w', encoding='utf-8') as papersDotTex:
    # with codecs.open('2016_Proceedings_ISMIR/papers.tex', 'w', 'utf-8') as papersDotTex:
    with open('2016_Proceedings_ISMIR/papers.tex', 'w') as papersDotTex:
        for title, authors, number, session in unicode_tsv_reader(csvFile):
            authors = andToComma(authors)
            for author in authors.split(', '):
                authorCount[author] += 1
                
            if session != lastSession:
                name, page = sessionInfo[session]
                papersDotTex.write(papersSectionHeader(name, page))
            lastSession = session
            
            papersDotTex.write('\includepaper{%s}{%s}{articles/%03d_Paper}\n'
                               % (latexEscape(title), authors, int(number)))

    #print sorted(authorCount.iteritems())
    print "Total authorings: %s" % sum(authorCount.values())
    print "Unique authors: %s" % len(authorCount)

def papersSectionHeader(name, page):
    chunk = """

\\thispagestyle{empty}\\cleardoublepage
\\addcontentsline{toc}{section}{%s}
\\includepdf[pages=%s,pagecommand=\\thispagestyle{empty}]{external/12_Sessions.pdf}%%
\\thispagestyle{empty}\\cleardoublepage

""" % (name, page)
    return chunk

def latexEscape(string):
    return string.replace('#','\#').replace('_','\_').replace('$','\$').replace('&','\&').replace('%','\%')

def andToComma(string):
    return string.replace(' and ', ', ')

def loadSessionInfo():
    return {k: (name, int(num)) for k, name, num
            in unicode_tsv_reader('data/sessionInfo.csv')}

    
def generateElectronicCsvFiles(csvFile):
    copySessionIndex()
    generateSessionFiles(csvFile)
    
def copySessionIndex():
    """Copy session_index file, created manually in excel.  Could
    maybe be created automatically from table of contents file from
    latex, but this is easier for now.

    """
    outFile = '2016_Proceedings_ISMIR_Electronic_Tools/data/session_index.csv'
    inFile  = 'data/session_index.csv'
    shutil.copy(inFile, outFile)
    
def generateSessionFiles(csvFile):
    sessionInfo = loadSessionInfo()
    sessions = collections.defaultdict(list)
    for title, authors, number, session in unicode_tsv_reader(csvFile):
        sessions[session].append((title, authors, int(number)))
    for session, info in sessions.iteritems():
        fileName = os.path.join('2016_Proceedings_ISMIR_Electronic_Tools/data',
                                '%s.csv' % session)
        makeDirs(os.path.dirname(fileName))
        with open(fileName, 'w') as sessionFile:
            sessionFile.write('Title;Authors;File\n')
            for title, authors, number in info:
                sessionFile.write('%s;%s;articles/%03d_Paper.pdf\n'
                                  % (title, authors, number))

def makeDirs(path):
    sub_path = os.path.dirname(path)
    if sub_path == path:
        raise "sub_path == path: %s" % path
    if len(sub_path) > 0 and not os.path.exists(sub_path):
        makeDirs(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

                
def main():
    csvFile = 'data/completePaperList.csv'
    generatePapersDotTex(csvFile)
    generateElectronicCsvFiles(csvFile)
    shutil.copy('data/reviewers.csv',
                '2016_Proceedings_ISMIR_Electronic_Tools/data/reviewers.txt')


if __name__ == '__main__':
    main()
    
