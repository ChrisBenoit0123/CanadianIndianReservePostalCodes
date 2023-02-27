import requests
from bs4 import BeautifulSoup

postal_codes_set = set()

# Read in all postal codes that have already been written to the file
try:
    with open('postal_codes.txt', 'r') as file:
        postal_codes_set = set(file.read().split(', '))
except FileNotFoundError:
    pass

with open('postal_codes.txt', 'a') as file:
    for i in range(6000, 12001):
        reserve_number = str(i).zfill(5)
        url = f'https://fnp-ppn.aadnc-aandc.gc.ca/FNP/Main/Search/RVDetail.aspx?RESERVE_NUMBER={reserve_number}&lang=eng'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            td_elements = soup.select('table tr td:nth-of-type(3)')
            if len(td_elements) > 0:
                postal_code = td_elements[-1].text.strip()[-7:].replace(' ', '')
                if postal_code not in postal_codes_set:
                    postal_codes_set.add(postal_code)
                    file.write(postal_code + ', ')
                    print(
                        f'Postal code for Reserve {reserve_number}: {postal_code}')
                else:
                    print(
                        f'Duplicate postal code {postal_code} found for Reserve {reserve_number}')
            else:
                print(f'No postal code found for Reserve {reserve_number}')
        else:
            print(f'Reserve {reserve_number} not found')
