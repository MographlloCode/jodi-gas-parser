"""
The `jodi_gas_series_parser` module is designed to automate the process of fetching,
extracting, and transforming gas production data from the Joint Organisations Data Initiative
(JODI) Gas Database into a structured and more usable JSON format.

This module performs several key operations:
    - Downloads a ZIP file containing the latest gas production data in CSV format from the JODI 
    website.
    - Extracts the CSV file from the ZIP archive and reads its contents.
    - Parses each row in the CSV to extract relevant information such as the time period, gas 
    production values, country codes, and other metadata.
    - Converts the time period format from the CSV into an ISO8601-compliant date format for 
    better interoperability.
    - Resolves country codes to country names by querying the REST Countries API, enriching 
    the dataset with more readable information.
    - Constructs a structured JSON object for each data series, including a unique identifier, 
    data points, and associated metadata.
    - Outputs the resulting collection of JSON objects into a file named `jodi_gas_info.json`, 
    ready for use in various data analysis, visualization, or storage applications.

This module is intended for data analysts, researchers, and developers who require access to JODI 
Gas production data in a more convenient format than the original CSV, and who wish to automate 
the process of data acquisition and transformation for their projects.

Dependencies:
    - datetime: For converting date formats.
    - urllib.request: For downloading files from the internet.
    - zipfile: For extracting ZIP archives.
    - io: For handling byte streams during file extraction.
    - csv: For reading and parsing CSV files.
    - json: For constructing and outputting JSON data.

Usage:
    Run the module directly as a script to initiate the data download, extraction, parsing, 
    and transformation process. Ensure you have an active internet connection and the necessary 
    permissions to write files to the destination directory.

Note:
    This module makes external requests to the JODI Gas Database and the REST Countries API. 
    Ensure compliance with their terms of use and be aware of any rate limits or restrictions.
"""


from datetime import datetime
import urllib.request
import zipfile
import io
import csv
import json

URL_PATH = 'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'
CSV_FILE_PATH = './src/jodi_gas_beta.csv'
REST_COUNTRIES_API_PATH = 'https://restcountries.com/v3.1/alpha/'

api_rest_countries_data_cache = {}

def date_to_iso_format(date:str) -> str:
    """ Method to convert JODI Gas CSV Datetime to ISO8601 format """
    date_object = datetime.strptime(date, '%Y-%m')
    iso_format_date = date_object.strftime('%Y-%m-%d')
    return iso_format_date

def download_and_extract_zip(zip_file_url:str) -> None:
    """ Method to download and extract Zip File """
    try:
        with urllib.request.urlopen(zip_file_url) as response:
            zip_file_content = response.read()
        zip_file = zipfile.ZipFile(io.BytesIO(zip_file_content))
        zip_file.extractall("./src")
    except Exception as e:
        print(f"error: {e}")

def get_country_name(country_code:str) -> str:
    """ Method that requests an External API to get Country Names """
    rest_countries_api_url = f"{REST_COUNTRIES_API_PATH}{country_code.lower()}"

    if country_code in api_rest_countries_data_cache:
        return api_rest_countries_data_cache[country_code]

    try:
        with urllib.request.urlopen(rest_countries_api_url) as response:
            data = response.read().decode("utf-8")
            country_data_list = json.loads(data)
            if country_data_list:
                country_data = country_data_list[0]
                country_name = country_data["name"]["common"]
                api_rest_countries_data_cache[country_code] = country_name
                return country_name
            else:
                return "not-found"
    except Exception as e:
        print(f"Error: {e}")
        return "not-found"

def read_and_parse_csv(csv_file_path):
    """ Method to read the csv file and parse data to desidered output """
    gas_data = []
    id = 0
    with open(csv_file_path, 'r', newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            gas_date = row['TIME_PERIOD']
            gas_production_value = row['OBS_VALUE']
            country_code = row['REF_AREA']
            energy_product = row['ENERGY_PRODUCT']
            flow_breakdown = row['FLOW_BREAKDOWN']
            measurement_unit = row['UNIT_MEASURE']
            jodi_assessment_code = row['ASSESSMENT_CODE']

            country_name = get_country_name(country_code)

            float_gas_production_value = float(gas_production_value)
            formatted_gas_date = date_to_iso_format(gas_date)

            series_id = f'{energy_product.lower()}{formatted_gas_date}{country_code}{id}{float(gas_production_value):.0f}gas-info'
            point = [formatted_gas_date, float_gas_production_value],
            fields = {
                "country": f"{country_name}",
                "concept": "Gas Production",
                "energy_product": f"{energy_product}",
                "flow_breakdown": f"{flow_breakdown}",
                "measurement_unit": f"{measurement_unit}",
                "jodi_assessment_code": f"{jodi_assessment_code}",
            }

            series_json = {
                "series_id": series_id,
                "points": [
                    point
                ],
                "fields": fields
            }

            gas_data.append(series_json)
            id += 1

    with open("./src/jodi_gas_info.json", 'w', encoding='utf-8') as json_file:
        json.dump(gas_data, json_file, indent=4, default=float)

    for series in gas_data:
        print(json.dumps(series, ensure_ascii=False))

download_and_extract_zip(URL_PATH)
read_and_parse_csv(CSV_FILE_PATH)
