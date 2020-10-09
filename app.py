from flask import Flask
import folium
import json
import pandas as pd

app = Flask(__name__)


def cases_df(case_type):
    sheet_name = 'Recent Sporadic Cases and Rates' if case_type == 'sporadic' else 'Recent Cases and Rates by Neigh'
    with open('./data/CityofToronto_COVID-19_NeighbourhoodData.xlsx', 'rb') as cases_data:
        df = pd.read_excel(cases_data, sheet_name=sheet_name)
    return df


def neighbourhood_geojson(df):
    with open('./data/Neighbourhoods.geojson') as geo_json:
        toronto_geo = json.load(geo_json)

    # create a dict to populate the case data to GeoJson due to current Folium limitation
    cases_dict = df.set_index('Neighbourhood ID').to_dict('index')

    # populate cases data to geojson
    for area in toronto_geo['features']:
        area_id = area['properties']['AREA_SHORT_CODE']
        if area_id in cases_dict:
            area['properties']['COVID_COUNT'] = cases_dict[area_id]['Case Count']
        else:
            area['properties']['COVID_COUNT'] = 0

    return toronto_geo


def neighbourhood_map(case_type):
    df = cases_df(case_type)
    geo_json = neighbourhood_geojson(df)

    start_coords = (43.72, -79.39)
    toronto_map = folium.Map(location=start_coords, zoom_start=11)

    choropleth = folium.Choropleth(
        geo_data=geo_json,
        name="Recent Toronto Covid-19",
        data=df,
        columns=['Neighbourhood ID', 'Case Count'],
        key_on='feature.properties.AREA_SHORT_CODE',
        fill_color='Reds',
        bins=9,
        fill_opacity=0.7,
        lin_opacity=0.2,
        highlight=True,
        legend_name='Toronto Area Covid-19 Recent Cases',
    ).add_to(toronto_map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['AREA_NAME', 'COVID_COUNT'],
            aliases=['Neighborhood: ', 'Recent Covid-19 Cases: '],
            style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
        )
    )

    toronto_map.keep_in_front(choropleth)
    folium.LayerControl().add_to(toronto_map)

    #toronto_map.save(outfile=r'C:\temp\toronto_map.html')

    return toronto_map


@app.route('/<case_type>')
def index(case_type='total'):
    return neighbourhood_map(case_type)._repr_html_()


if __name__ == '__main__':
    app.run()

