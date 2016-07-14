#!/usr/bin/python

import csv
import os
import PyPDF2
from ismir_utils import unicode_csv_reader, search_pages_total, makeDirs


def main():
    # open proceedings
    proceedings_pdf = PyPDF2.PdfFileReader(open('data/2016_Proceedings_ISMIR.pdf', 'rb'))

    # open pages_total as look-up table
    with open('data/pages_total.csv') as pages_total:
        pt_reader = unicode_csv_reader(pages_total, delimiter=';')
        next(pt_reader) # skip the headers

        # store it all in a list
        pages_total = list(pt_reader)


    with open('data/session_index.csv') as session_index:
        si_reader = unicode_csv_reader(session_index, delimiter=';')
        next(si_reader) # skip the headers

        # iterate over sessions
        for session_name, start_page, header_name in si_reader:
            print "Session name:" +session_name,"Starting Page:" +start_page

            # open session file
            with open('data/' + session_name + '.csv') as current_session: #define session_name.csv as the current_session
                s_reader = unicode_csv_reader(current_session, delimiter=';')
                next(s_reader) # skip the headers

                # iterate over session entries
                current_paper_start = int(start_page)
                for paper_title, authors, pdf_filename in s_reader:
                    # get number of pages for this paper
                    current_paper = pdf_filename
                    print current_paper
                    pdf_filename = pdf_filename.split('/')[1] #split and take the part after "/"
                    print "Current paper being processed: " + pdf_filename
                    # search for it in the pages_total
                    current_paper_length = search_pages_total(current_paper, pages_total)

                    current_paper_end = current_paper_start+current_paper_length-1
                    #current_paper_end = 0
                    print "Start page: " +str(current_paper_start)
                    print  "End page: " +str(current_paper_end)


                    output = PyPDF2.PdfFileWriter()
                    for p in range(current_paper_start-1, current_paper_end):
                        print p
                        output.addPage(proceedings_pdf.getPage(p))

                    #output_folder = 'output/articles'
                    output_folder = 'data/articles_splitted'
                    makeDirs(output_folder)
                    with open(output_folder + '/' + pdf_filename, 'wb') as f:
                        output.write(f)

                    current_paper_start = current_paper_end + 1


if __name__ == '__main__':
    main()
    
