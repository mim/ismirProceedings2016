#!/usr/bin/python

import codecs
import csv
import jinja2
import os
from ismir_utils import unicode_csv_reader, search_pages_total, makeDirs


# open pages_total as look-up table
with open('data/pages_total.csv') as pages_total:
    pt_reader = unicode_csv_reader(pages_total, delimiter=';')
    next(pt_reader) # skip the headers
    
    # store it all in a list
    pages_total = list(pt_reader)

sessions = []
pdf_offset = 28

with open('data/session_index.csv') as session_index:
    si_reader = unicode_csv_reader(session_index, delimiter=';')
    next(si_reader) # skip the headers

    # iterate over sessions
    for session_name, start_page, header_name in si_reader:
        print session_name, start_page

        current_paper_start = int(start_page)
        # open session file
        with open('data/' + session_name + '.csv') as current_session:
            s_reader = unicode_csv_reader(current_session, delimiter=';')
            next(s_reader) # skip the headers

            # iterate over session entries
            publications = []
            for paper_title, authors, pdf_filename in s_reader:
                current_paper = pdf_filename
                current_paper_length = search_pages_total(current_paper, pages_total)
                current_paper_end = current_paper_start+current_paper_length-1
                publications.append({'title': paper_title,
                                     'authors': authors,
                                     'paper_startpage': current_paper_start-pdf_offset,
                                     'paper_endpage': current_paper_end-pdf_offset,
                                     'pdf': pdf_filename})
                current_paper_start = current_paper_end + 1

        sessions.append({'title': header_name,
                         'publications': publications})

context = {
        'sessions': sessions
    }

# get jinja template
PATH = os.path.dirname(os.path.abspath(__file__))
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(PATH, 'templates')))
template = template_env.get_template('overview_table.html')

makeDirs('output/html_overview_table')
with open('output/html_overview_table/index.html', 'w') as f:
    html = template.render(context)
    f.write(html.encode('utf-8'))

template = template_env.get_template('overview_table.html')
with open('output/overview_table.html', 'w') as f:
    html = template.render(context)
    f.write(html.encode('utf-8'))

template = template_env.get_template('dblp.txt')
with open('output/publications_ISMIR2016.txt', 'w') as f:
    html = template.render(context)
    f.write(html.encode('utf-8'))
