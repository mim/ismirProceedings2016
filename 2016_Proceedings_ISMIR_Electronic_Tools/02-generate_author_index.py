#!/usr/bin/python

import csv
import codecs
import jinja2
import os
from nameparser import HumanName
from ismir_utils import search_pages_total, unicode_csv_reader
import string


# open pages_total as look-up table
with open('data/pages_total.csv') as pages_total:
    pt_reader = unicode_csv_reader(pages_total, delimiter=';')
    next(pt_reader) # skip the headers
    
    # store it all in a list
    pages_total = list(pt_reader)

# get jinja template
PATH = os.path.dirname(os.path.abspath(__file__))
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(PATH, 'templates')))
template = template_env.get_template('author_index.html')

publications = []
unique_authors =[]
pdf_offset = 28

with open('data/session_index.csv') as session_index:
    si_reader = unicode_csv_reader(session_index, delimiter=';')
    next(si_reader) # skip the headers

    # iterate over sessions
    for session_name, start_page, header_name in si_reader:
        # open session file
        with open('data/' + session_name + '.csv') as current_session:
            s_reader = unicode_csv_reader(current_session, delimiter=';')
            next(s_reader) # skip the headers

            # iterate over session entries
            current_paper_start = int(start_page)
            for paper_title, authors, pdf_filename in s_reader:
                current_paper = pdf_filename
                pdf_filename = pdf_filename.split('/')[1] #split and take the part after "/"
                # search for it in the pages_total
                current_paper_length = search_pages_total(current_paper, pages_total)
                current_paper_end = current_paper_start+current_paper_length-1

                for author in authors.split(','):
                    author = author.strip()
                    search_author = filter(lambda cur_author: cur_author['name'] == author, unique_authors)
                    if not search_author:
                        # append to list
                        unique_authors.append({'name': author,
                                               'human_name': HumanName(author),
                                               'pdfs': [pdf_filename, ],
                                               'paper_startpage': [current_paper_start-pdf_offset, ],
                                               'paper_title': [paper_title, ]})
                    else:
                        search_author[0]['pdfs'].append(pdf_filename)
                        search_author[0]['paper_startpage'].append(current_paper_start-pdf_offset)
                        search_author[0]['paper_title'].append(paper_title)

                current_paper_start = current_paper_end + 1


context = {
        'unique_authors': unique_authors,
        'abc': string.uppercase
    }

with open('output/html_overview_table/author_index.html', 'w') as f:
    html = template.render(context)
    new_html = str()
    for line in html.split('\n'):
        if line != '':
            new_html += line + '\n'

    print type(html)
    f.write(new_html.encode('utf-8'))
