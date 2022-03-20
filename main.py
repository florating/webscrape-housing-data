import csv
import os
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup


HOUSING_SITES = [
    # 'https://housing.uci.edu/campus-village/',
    'https://housing.uci.edu/palo-verde/',
    'https://housing.uci.edu/verano-place/',
]


_FILEPATH = os.path.abspath('./data/')


def get_housing_name(filepath):
    """
    >>> get_housing_name('https://housing.uci.edu/palo-verde/')
    'Palo Verde'
    """
    end_pos = re.search('https://housing.uci.edu/', filepath).end()
    name = filepath[end_pos:-1]
    return name.replace('-', ' ').title()

def get_table_headers(table):
    headers = table.thead.tr.contents
    if headers is None:
        print('Did not find headers.')
    else:
        values = []
        for val in headers:
            # val.contents --> ['# of', <br/>, 'Bedrooms'] or '\n'
            if val == '\n':
                continue
            elif isinstance(val, str):
                values.append(val)
                continue
            clean_val = ''
            for child in val.children:
                if isinstance(child, str):
                    clean_val += child
                else:
                    s = child.string
                    clean_val += s if isinstance(s, str) else ' '
            values.append(clean_val.strip())
        print(values)
        return values

    
def get_table_body(table):
    content = table.tbody.find_all('tr')

    if content is None:
        print('Did not find content.')
    else:
        values = []
        for child_row in content:
            # print(child_row.stripped_strings)
            row = get_values_from_row(child_row.contents)
            # print(row)
            plan_url = get_floor_plan(child_row.a)
            if plan_url:
                row.append(plan_url)
            values.append(row)
        print(values)
        return values


def get_values_from_row(row):
    values = []
    for val in row:
        # val.contents --> ['# of', <br/>, 'Bedrooms'] or '\n'
        if val == '\n':
            continue
        elif isinstance(val, str):
            values.append(val)
            continue
        else:
            # clean_val = ''
            # for child in val.children:
            #     if isinstance(child, str):
            #         clean_val += child
            #     else:
            #         s = child.string
            #         clean_val += s if isinstance(s, str) else ' '
            values.append(val.text.strip())
    return values


def get_floor_plan(a_tag):
    return a_tag['href']


def scrape_table_headers(url):
    with urlopen(url) as webpage:
        soup = BeautifulSoup(webpage, features='html.parser')

        title = soup.find('meta', attrs={'property': 'og:title'})
        title_content = title['content'] if title else 'No meta title given'
        print(title_content)

        image = soup.find('meta', {'property': 'og:image'})
        image_content = image['content'] if image else 'No meta url given'
        print(image_content)

        return (title, title_content, image, image_content)


def write_data_to_csv(val_list, table_name):
    """val_list: list containing a list of elements for each table row"""
    summary = []

    altered_name = table_name.replace(' ', '_').lower()

    file = f'{_FILEPATH}/{altered_name}.csv'
    print(file)

    with open(file, mode='a', encoding='utf-8') as data:
        data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for result in val_list:
            if not result:
                continue
            data_writer.writerow(result)
            summary.append(result)
    
    print('Done with write_data_to_csv!')
    return summary


def main():
    for site_url in HOUSING_SITES:
        site_name = get_housing_name(site_url)

        with urlopen(site_url) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

            table_tag = soup.table
            header_list = get_table_headers(table_tag)
            body_list = get_table_body(table_tag)

            write_data_to_csv([header_list], site_name)
            write_data_to_csv(body_list, site_name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    main()
