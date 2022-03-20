import csv
import io
import os
from pprint import pprint
import urllib.request as req

from PyPDF2 import PdfFileMerger
from reportlab.pdfgen.canvas import Canvas

import pdf_writer


FILES = {
    'palo-verde': './data/palo_verde.csv',
    'verano-place': './data/verano_place.csv',
}


def get_all_data(filepath):
    """Return list of dicts per row of data scraped from the housing webpages."""
    urls = []

    with open(filepath, mode='r', encoding='utf-8') as metadata:
        csvreader = csv.DictReader(metadata)

        for row in csvreader:
            print(row)
            row['Floor Plan'] = create_file_name(row.get('Floor Plan'))
            urls.append(row)
    
    print(f'\n\nSuccessfully found {len(urls)} rows with urls.\n\n')
    return urls


def get_pdf_urls(data_list):
    """Returns dict of floor plan names (keys) and non-local pdf URLs (values)."""
    urls = {}
    for row in data_list:
        name = row.get('Floor Plan')
        urls[f'{name}'] = row.get('pdf_url')
    return urls


def create_file_name(plan):
    return plan.lower().replace(' ', '-')


def download_pdfs(folder, urls, can_download=False, can_overwrite=False):
    """Downloads PDF files given a list of urls from get_pdf_urls.

    Parameters:
        - folder: absolute path for ./data/palo-verde-pdfs (or similar)
        - urls: list of absolute paths for {folder}/unit-a.pdf, etc

    Returns: a dict of floor plan names (eg: 'unit-a') and local paths for the downloaded PDF.
        - keys: floor plan names (eg: 'unit-a')
        - values: list of local paths for the now-downloaded PDF
        - eg: {
                'unit-a': '/Users/.../data/palo-verde-pdfs/unit-a.pdf',
                'unit-b': '/Users/.../data/palo-verde-pdfs/unit-b.pdf',
                ...
            }
    """
    files = {}
    open_mode = 'wb+' if can_overwrite else 'wb'
    print(f'can_download={can_download}, can_overwrite={can_overwrite}:')
    for plan_name, url in urls.items():
        filename = f'{folder}/{plan_name}.pdf'
        if can_download:
            with open(filename, open_mode) as f:
                response = req.urlopen(url)
                f.write(response.read())
            print(f'Finished downloading {filename}')
        else:
            print(f'filename = {filename}')
        files[plan_name] = filename
    return files


# def write_info_to_pdf(info_dict, pdf):
#     """
#     info_dict keys are:
#         Floor Plan,
#         # of Bedrooms,
#         # of Baths,
#         Sq. Ft.,
#         Full Unit1,
#         Single Students2,
#         pdf_url
#     """
#     canvas = Canvas(pdf)
#     unwanted_keys = {'Floor Plan', 'Sq. Ft.', 'pdf_url'}
#     x = 0
#     for key, val in info_dict.items():
#         if key not in unwanted_keys:
#             canvas.setFont('Helvetica', 10)
#             canvas.drawString(700, 72 + (16 * x), f'{key:<30}: {val}')
#             x += 1
#     canvas.save()
#     print(f'Finished writing to {pdf}!')


def merge_files_into_multi_pdf(files, destination):
    """Merge list of PDF files (absolute paths) and save to destination (path).

    Parameters:
    - files: a list of absolute paths for written PDFs (eg: '/Users/.../data/palo-verde-pdfs/v2/unit-a.pdf')
    - destination: a filepath (eg: absolute path for '{pdf_path}/v2/all_plans_v2.pdf')
    """
    if not files:
        print('There are no files to merge.')
        return

    user_confirmation = input(f'Are you sure you want to merge these {len(files)} file(s) to {destination}? (type "yes" if you do) ')
    if user_confirmation == 'yes':
        pdf_merger = PdfFileMerger()
        # add filepaths to pdf_merger
        for path in files:
            # print(path)
            pdf_merger.append(str(path))

        with open(destination, mode='wb+') as output_file:
            pdf_merger.write(output_file)


if __name__ == '__main__':
    for housing, file in FILES.items():
        filepath = os.path.abspath(file)

        # get PDF urls (list)
        data = get_all_data(filepath)
        urls = get_pdf_urls(data)

        # set the local path
        house_dir = f'{housing}-pdfs'  # eg: 'palo-verde-pdfs'
        pdf_path = os.path.abspath(f'./data/{house_dir}/')

        # download PDF files
        download_option = input(f'Do you want to download new data for {house_dir}? (press ENTER if not) ')
        overwrite_option = input('Do you want to overwrite existing data? (press ENTER if not) ') if bool(download_option) else False
        local_paths_dict = download_pdfs(
            pdf_path,   # absolute path for ./data/palo-verde-pdfs (or similar)
            urls,       # list of absolute paths for {pdf_path}/unit-a.pdf, etc
            can_download=bool(download_option),
            can_overwrite=bool(overwrite_option)
        )
        
        # edit individual PDF files to add housing info (each row of the table)
        written_files_list = pdf_writer.main(house_dir = house_dir, dataset = data)
        destination=f'{pdf_path}/v2/{housing.replace("-","_")}-all_plans_v2.pdf'
        merge_files_into_multi_pdf(written_files_list, destination)  
