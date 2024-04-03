# JODI Gas Data Series Parser

This Python script is designed to fetch, parse, and transform gas production data from the JODI Gas Database into a structured JSON format. The script downloads a ZIP file containing CSV data, extracts the contents, reads the CSV file, and outputs JSON data with additional information such as country names resolved through an external API.

## Features

- **Data Download**: Automatically downloads the latest JODI Gas CSV data from a predefined URL.
- **ZIP File Handling**: Extracts the ZIP file to access the CSV data.
- **Data Parsing**: Parses each row of the CSV to extract and transform gas production data.
- **Date Formatting**: Converts the JODI Gas CSV datetime format to ISO8601.
- **Country Name Resolution**: Enhances the dataset by adding country names using the REST Countries API, based on country codes from the CSV.
- **JSON Output**: Outputs the transformed data into a JSON file with a structured format suitable for various applications.

## Prerequisites

Before running this script, ensure you have Python installed on your system. The script uses the following Python modules, which should be available in a standard Python environment:

- `datetime`
- `urllib.request`
- `zipfile`
- `io`
- `csv`
- `json`

## Usage

To use this script, simply run it from your command line:

```bash
python jodi_gas_series_parser.py
```

## The script will perform the following actions:

1. Download the ZIP file from the JODI Gas Database.
2. Extract the ZIP file to access the CSV data.
3. Read and parse the CSV data, transforming it into a structured JSON format.
4. Save the JSON data to a file named jodi_gas_info.json in the ./src directory.

## Output Format
The output JSON data will have the following structure for each series of gas data:

```json
{
  "series_id": "<unique identifier for the data series>",
  "points": [
    ["<date in ISO8601 format>", <gas production value>]
  ],
  "fields": {
    "country": "<country name>",
    "concept": "Gas Production",
    "energy_product": "<energy product>",
    "flow_breakdown": "<flow breakdown>",
    "measurement_unit": "<measurement unit>",
    "jodi_assessment_code": "<JODI assessment code>"
  }
}
```

## Contributing
Contributions to improve this script are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This script is provided "as is", without warranty of any kind. You are free to use, modify, and distribute it as you see fit.

## Disclaimer
This script is not affiliated with, endorsed by, or in any way officially connected with the JODI Gas Database, REST Countries API, or any other entity involved in providing the data used by this script.

## Author
<div style='display: flex; align-items: center; gap: 8px'>
    <img src='https://media.licdn.com/dms/image/D4D03AQH66gZ5k8A8Ew/profile-displayphoto-shrink_200_200/0/1709477885353?e=1717632000&v=beta&t=lJ0gAqt43dCjRm_IdV7qR6jdvNfqn_EGl2iWm0Goz2I' width='128' height='128' style='border-radius: 100%; border: 2px solid #f9f9f9'></img>
    <div>
        <h3 style='font-family: sans-serif; font-size: 2rem; line-height: 8px;'>Gustavo Mello</h3>
        <p style='font-size: 1.2rem; line-height: 20px; margin-top: -8px;'>Back End Developer | Python | Django | Flask | AWS | SQL | MySQL | PostgreSQL</p>
        <a href='https://www.linkedin.com/in/mographllo/'>
            <img src='https://th.bing.com/th/id/R.3ffcfcb93b1527cb663e7da9ac9c0ea5?rik=9tOIpBbhMTi0tA&pid=ImgRaw&r=0' height='32'></img>
        </a>
        <a href='https://www.tiktok.com/@ogusmello/'>
            <img src='https://logodownload.org/wp-content/uploads/2019/08/tiktok-logo-icon.png' height='32'></img>
        </a>
        <a href='mailto:contact@gmello.tech'>
            <img src='https://pngimg.com/uploads/gmail_logo/gmail_logo_PNG1.png' height='30'></img>
        </a>
    </div>
</div>
