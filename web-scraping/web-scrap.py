"""
This is the code for web scrapping from a website named Box Office Mojo.
https://www.boxofficemojo.com

I've used Pandas module, requests module and requests_html module.

-> requests module help to access the website and get the data as a plain text.
-> requests_html module helps to extract HTML elements from the plain text.
-> pandas module is used to write the csv file.
"""

import os
import sys
import datetime
import requests
import pandas as pd
from requests_html import HTML

# Define bsae dir
BASE_DIR = os.path.dirname(__file__)

# Set current year
now = datetime.datetime.now()
current_year = now.year


# Takes the HTML data from website and returns it
def url_to_txt(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    return None


def parse_and_extract(url, file_name=current_year):
    '''
    Parse the HTML data and extract fields
    Store that data in the list
    Write the data of list in the CSV file
    '''

    # Convert data of URL to plain text
    html_text = url_to_txt(url)
    if html_text is None:
        return False

    r_html = HTML(html=html_text)

    # Unique identifier to find the required data
    table_class = ".imdb-scroll-table"

    # Get the data of table
    r_table = r_html.find(table_class)

    # If there's no data, return False
    if len(r_table) == 0:
        return False

    table_data = []
    header_names = []

    parsed_table = r_table[0]

    # Find the rows of parsed table
    rows = parsed_table.find("tr")

    # The table has a header
    header_row = rows[0]
    header_cols = header_row.find('th')
    header_names = [header.text for header in header_cols]

    for row in rows[1:]:
        row_data = []
        cols = row.find("td")

        for i, col in enumerate(cols):
            row_data.append(col.text)

        table_data.append(row_data)

    # Parse data as Data Frame by Pandas
    df = pd.DataFrame(table_data, columns=header_names)

    # Define path of file
    folder_path = os.path.join(BASE_DIR, 'data')
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join('data', f'{file_name}.csv')

    # Write data in CSV file by Data Frame
    df.to_csv(filepath, index=False)
    return True


# Main function
def run(start_year=current_year, years_ago=0):
    # Check for the valid start year
    if len(f"{start_year}") == 4:
        for _ in range(years_ago+1):
            # Url to scrap
            url = f"https://www.boxofficemojo.com/year/world/{start_year}/"

            extraction_status = parse_and_extract(url, file_name=start_year)
            if extraction_status:
                print(f"Finished {start_year}")
            else:
                print(f"{start_year} not finished")
            start_year -= 1
    else:
        print("Please enter a valid start year!!")


if __name__ == "__main__":
    start_time = datetime.datetime.now().timestamp()
    print(f"Started at {start_time}")

    # Take start year
    try:
        start_year = int(sys.argv[1])
    except Exception:
        start_year = current_year

    # Take end year
    try:
        years_ago = int(sys.argv[2])
    except Exception:
        years_ago = 0

    # Call the main function
    run(start_year=start_year, years_ago=years_ago)

    end_time = datetime.datetime.now().timestamp()
    print(f"Ended at {end_time}")

    time_elapsed = int(end_time - start_time)
    print(f"Total time elapsed = {time_elapsed} seconds")
