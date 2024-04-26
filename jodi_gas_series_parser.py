from datetime import datetime
import urllib.request
import zipfile
import io
import csv
import json

URL_PATH = 'https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip'

def date_to_iso_format(date:str) -> str:
    date_object = datetime.strptime(date, '%Y-%m')
    iso_format_date = date_object.strftime('%Y-%m-%d')
    return iso_format_date

def download_and_read_csv(zip_file_url:str) -> dict:
    try:
        with urllib.request.urlopen(zip_file_url) as response:
            zip_file_content = response.read()

        zip_file = zipfile.ZipFile(io.BytesIO(zip_file_content))
        csv_file_name = next((name for name in zip_file.namelist() if name.endswith('.csv')), None)
        if csv_file_name is None:
            print("No CSV file found in the ZIP archive.")
            return None

        csv_file = zip_file.open(csv_file_name)
        csv_reader = csv.DictReader(io.TextIOWrapper(csv_file, encoding='utf-8'))
        return csv_reader

    except Exception as e:
        print(f"Error: {e}")
        return None

def read_and_parse_csv():
    csv_reader = download_and_read_csv(URL_PATH)
    if csv_reader is None:
        print("Failed to read CSV from ZIP file.")
        return
    
    series_dict = {}
    
    for row in csv_reader:
        gas_date = row['TIME_PERIOD']
        gas_production_value = float(row['OBS_VALUE'])
        country_code = row['REF_AREA']
        energy_product = row['ENERGY_PRODUCT']
        flow_breakdown = row['FLOW_BREAKDOWN']
        measurement_unit = row['UNIT_MEASURE']
        jodi_assessment_code = row['ASSESSMENT_CODE']
        formatted_gas_date = date_to_iso_format(gas_date)

        series_key = f'{country_code}-{energy_product}'

        if series_key not in series_dict:
            series_dict[series_key] = {
                "series_id": f'{energy_product.lower()}-{country_code}-gas-info',
                "points": {},
                "fields": {
                    "country": country_code,
                    "concept": "Gas Production",
                    "energy_product": energy_product,
                    "flow_breakdown": flow_breakdown,
                    "measurement_unit": measurement_unit,
                    "jodi_assessment_code": jodi_assessment_code,
                }
            }

        if formatted_gas_date in series_dict[series_key]["points"]:
            existing_data = series_dict[series_key]["points"][formatted_gas_date]
            new_avg = (existing_data[0] * existing_data[1] + gas_production_value) / (existing_data[1] + 1)
            series_dict[series_key]["points"][formatted_gas_date] = (new_avg, existing_data[1] + 1)
        else:
            series_dict[series_key]["points"][formatted_gas_date] = (gas_production_value, 1)

    for series in series_dict.values():
        series["points"] = [[date, value[0]] for date, value in series["points"].items()]

    with open("./jodi_gas_info.json", 'w', encoding='utf-8') as json_file:
        json.dump(list(series_dict.values()), json_file, indent=4, default=float)

    for series in series_dict.values():
        print(json.dumps(series, ensure_ascii=False))

read_and_parse_csv()
