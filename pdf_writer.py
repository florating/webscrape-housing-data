import io
import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter


EXAMPLE_DATASET = [
    {
        'Floor Plan': 'unit-a',
        '# of Bedrooms': 'studio',
        '# of Baths': '1 Ba',
        'Sq. Ft.': '411',
        'Full Unit1': '$942',
        'Single Students2': '$942',
        'pdf_url': 'https://sites.uci.edu/ucihousing/files/2021/05/PV_Unit-A.pdf'
    },
    {
        'Floor Plan': 'unit-b',
        '# of Bedrooms': '1 Br',
        '# of Baths': '1 Ba',
        'Sq. Ft.': '600',
        'Full Unit1': '$1,186',
        'Single Students2': '$1,186',
        'pdf_url': 'https://sites.uci.edu/ucihousing/files/2021/05/PV_Unit-B.pdf'
    },
]

DESIRED_FIELDS = {
    '# of Bedrooms': '',
    '# of Baths': '',
    'Sq. Ft.': '',
    'Full Unit1': 'Full Unit',
    'Single Students2': 'Single Student',
}

DATA_DIR = os.path.abspath('./data/')

HOUSING_DIR = {
    'palo-verde-pdfs',
    'verano-place-pdfs',
}

# ORIG_EXAMPLE = f'{DATA_DIR}/palo-verde-pdfs/example.pdf'
ORIG_EXAMPLE = f'{DATA_DIR}/palo-verde-pdfs/all_plans.pdf'

COPY_EXAMPLE = f'{DATA_DIR}/palo-verde-pdfs/example-copy.pdf'


def format_message(data, fields=DESIRED_FIELDS, spacing=18):
    message = ''
    for key, val in data.items():
        if key in fields:
            field = fields[key] if fields[key] else key
            message += f'{field:>{spacing}}: {val:<{spacing // 2}}'
    return message


def write_to_single_pdf(message, destination=COPY_EXAMPLE, origin=ORIG_EXAMPLE, can_overwrite=False):
    packet = io.BytesIO()
    canvas = Canvas(packet, pagesize=letter)
    canvas.drawString(10, 10, f'{message}')
    canvas.save()

    # move to the beginning of the BytesIO buffer
    packet.seek(0)

    new_pdf = PdfFileReader(packet)

    existing_pdf = PdfFileReader(open(origin, 'rb'))
    print(f'just opened {origin}')
    output = PdfFileWriter()

    # add the new_pdf content as a "watermark" onto existing_pdf
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # write output to a real file
    write_mode = 'wb+' if can_overwrite else 'wb'
    with open(destination, write_mode) as output_stream:
        output.write(output_stream)
    print(f'finished writing to {destination}')


def main(house_dir, dataset=EXAMPLE_DATASET):
    """Returns a dict after writing data to single PDF files when given a dataset.

    Parameters:
    - house_dir: 'palo-verde-pdfs' or 'verano-place-pdfs'
    - dataset: defaults to EXAMPLE_DATASET

    Returns: a list of new (absolute) filepaths, all within the /v2 directory
    - eg: [
            '{path_dir}/v2/unit-a.pdf',
            '{path_dir}/v2/unit-b.pdf',
            ...
    ]
    """
    
    cont = input(f'Do you want to write to files in {house_dir}? (press ENTER if not) ')
    if not cont:
        return

    path_dir = f'{DATA_DIR}/{house_dir}' if 'data' not in house_dir else house_dir

    overwrite_option = True if input('Do you want to overwrite destination files? (type "yes" if you do) ') == 'yes' else False
    written_files = []

    for data in dataset:
        origin_file_path = f'{path_dir}/{data["Floor Plan"]}.pdf'
        dest_file_path = f'{path_dir}/v2/{data["Floor Plan"]}.pdf'

        written_files.append(dest_file_path)
        message = format_message(data)
        write_to_single_pdf(message, destination=dest_file_path, origin=origin_file_path, can_overwrite=overwrite_option)
    return written_files
