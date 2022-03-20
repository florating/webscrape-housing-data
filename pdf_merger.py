import csv
import os
import urllib.request as req

from PyPDF2 import PdfFileMerger


FILES = {
    'palo-verde': './data/palo_verde.csv',
    # 'verano-place': './data/verano_place.csv',
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
    """Returns dict of floor plan names (keys) and pdf URLs (values)."""
    urls = {}
    for row in data_list:
        name = row.get('Floor Plan')
        urls[f'{name}'] = row.get('pdf_url')
    return urls


def create_file_name(plan):
    return plan.lower().replace(' ', '-')


def download_pdfs(folder, urls):
    """Return dict of floor plan names (eg: Unit A) and local urls for the downloaded PDF."""
    files = {}
    for plan_name, url in urls.items():
        filename = f'{folder}/{plan_name}.pdf'
        with open(filename, 'wb+') as f:
            # response = req.urlopen(url)
            # f.write(response.read())
            print(f'Finished downloading {filename}')
        files[plan_name] = filename
    return files
        

if __name__ == '__main__':
    for housing, file in FILES.items():
        filepath = os.path.abspath(file)

        # get PDF urls (list)
        data = get_all_data(filepath)
        urls = get_pdf_urls(data)
        # print(urls)

        # set the local path
        house_dir = f'{housing}-pdfs'
        pdf_path = os.path.abspath(f'./data/{house_dir}/')

        # download PDF files
        house_plans = download_pdfs(pdf_path, urls)

        # add filepaths to pdf_merger
        pdf_merger = PdfFileMerger()
        for path in house_plans.values():
            print(path)
            pdf_merger.append(str(path))

        with open(f'{pdf_path}/all_plans.pdf', mode='wb+') as output_file:
            pdf_merger.write(output_file)
