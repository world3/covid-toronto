import requests

# Download the Cases Excel Sheet
url = r'https://docs.google.com/spreadsheets/d/1jzH64LvFQ-UsDibXO0MOtvjbL2CvnV3N/export?format=xlsx'

r = requests.get(url, allow_redirects=True)

open(r'C:\temp\CityofToronto_COVID-19_NeighbourhoodData.xlsx', 'wb').write(r.content)

