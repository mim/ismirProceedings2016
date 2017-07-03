# ISMIR Proceedings 2016

Scripts for generating ISMIR 2016 proceedings

## Directories in this repository

| Directory | Purpose |
| --- | --- |
| `./` | Scripts for global processing |
| `data/` | Input: Metadata about papers, sessions, etc |
| `2016_Proceedings_ISMIR/articles/` | Input: PDF files of all articles by number, e.g., `004_Paper.pdf` |
| `2016_Proceedings_ISMIR/external/` | Input: Front matter created in Word or google docs |
| `2016_Proceedings_ISMIR_Electronic_Tools/templates/` | Input: templates for HTML proceedings, DBLP |
| `2016_Proceedings_ISMIR/` | LaTeX files for generating PDF proceedings |
| `2016_Proceedings_ISMIR_Electronic_Tools/` | Scripts for generating HTML proceedings for USB sticks |
| `2016_Proceedings_ISMIR_Electronic/` | Output: some HTML proceedings files |
| `2016_Proceedings_ISMIR_Electronic_Tools/output/` | Output: other HTML proceedings files |

## Steps to run scripts and generate PDF and HTML proceedings

1. Import paper metadata into `data/completePaperList.xlsx`
1. Export CSV file from the first sheet in that file (`paperList.txt`) to `data/completePaperList.csv`
1. Import session metadata into the `sessions` sheet, export to `data/sessionInfo.csv`
1. Modify other sheets and export to corresponding csv files as necessary
1. Run `./deriveFiles.py` to derive other metadata files from those
1. Create directory (or link) `2016_Proceedings_ISMIR/articles/` containing the camera-ready PDFs
1. Run `2016_Proceedings_ISMIR/01-get_pages_total.py` to calculate page lengths of files for indexing purposes
1. Run `2016_Proceedings_ISMIR/00-run.sh` to compile the PDF proceedings
1. Copy or link the compiled proceedings to `2016_Proceedings_ISMIR_Electronic_Tools/data/2016_Proceedings_ISMIR.pdf`
1. Run `2016_Proceedings_ISMIR_Electronic_Tools/00-split_proceedings.py`
1. Run `2016_Proceedings_ISMIR_Electronic_Tools/01-generate_overview_website.py`
1. Run `2016_Proceedings_ISMIR_Electronic_Tools/02-generate_author_index.py`
1. Run `2016_Proceedings_ISMIR_Electronic_Tools/03-generate_reviewer_list.py`
