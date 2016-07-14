#!/usr/bin/python

import PyPDF2
import glob

all_pdf_files = glob.glob('articles/*.pdf')
with open('../2016_Proceedings_ISMIR_Electronic_Tools/data/pages_total.csv', 'w') as f:
    f.write('filename,pages_total\n')

    for cur_pdf_filename in all_pdf_files:
        with open(cur_pdf_filename, 'rb') as cur_pdf_fh:
            cur_pdf = PyPDF2.PdfFileReader(cur_pdf_fh)
            f.write(cur_pdf_filename + ',' + str(cur_pdf.getNumPages()) + '\n')
