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
            else:
                values.append(val.text.strip())
        print(values)
        return values

    
def get_table_body(table):
    content = table.tbody.find_all('tr')

    if content is None:
        print('Did not find content.')
    else:
        values = []
        for child_row in content:
            row = get_values_from_row(child_row.contents)
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
            values.append(val.text.strip())
    return values


def get_floor_plan(a_tag):
    return a_tag['href']


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
