#####
# Setting environment variable. NOTE: This is not a production-safe practice.
# This is only acceptable because this is a lab.
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/tushimin/Desktop/musa-509-final-27b36afe08d2.json'
#####
import geopandas as gpd
import pandas as pd
from pathlib import Path
from tempfile import NamedTemporaryFile
from jinja2 import Environment, FileSystemLoader


template_root = Path(__file__).parent / 'templates'
output_root = Path(__file__).parent.parent / 'output'

def main():
    # Download the neighborhood list data.
    neighborhood_df =pd.read_gbq('SELECT * FROM justtest.neighborhood_list')

    # Download the neighborhood map data.
    neigh_mapdata_df = pd.read_gbq('SELECT * FROM justtest.gro_in_neigh')
    neigh_mapdata_df.neigh_geom = gpd.GeoSeries.from_wkt(neigh_mapdata_df.neigh_geom)
    neigh_mapdata_gdf= gpd.GeoDataFrame(neigh_mapdata_df, geometry='neigh_geom')

    # Download the grocery map data.
    gro_mapdata_df = pd.read_gbq("SELECT * FROM justtest.gro_in_neigh")
    gro_mapdata_df.gro_geom = gpd.GeoSeries.from_wkt(gro_mapdata_df.gro_geom)
    gro_mapdata_gdf = gpd.GeoDataFrame(gro_mapdata_df, geometry='gro_geom')  

    # Download the restaurant map data.
    res_mapdata_df = pd.read_gbq("SELECT * FROM justtest.res_in_neigh")
    res_mapdata_df.res_geom = gpd.GeoSeries.from_wkt(res_mapdata_df.res_geom)
    res_mapdata_gdf = gpd.GeoDataFrame(res_mapdata_df, geometry='res_geom')  

    # Download the bus stop map data.
    bus_mapdata_df = pd.read_gbq("SELECT * FROM justtest.bus_in_neigh")
    bus_mapdata_df.stop_geom = gpd.GeoSeries.from_wkt(bus_mapdata_df.stop_geom)
    bus_mapdata_gdf = gpd.GeoDataFrame(bus_mapdata_df, geometry='stop_geom')  

    # Download the all crime map data.
    crime_risk_mapdata_df = pd.read_gbq('SELECT * FROM justtest.crime_risk')
    crime_risk_mapdata_df.the_geom = gpd.GeoSeries.from_wkt(crime_risk_mapdata_df.the_geom)
    crime_risk_mapdata_gdf = gpd.GeoDataFrame(crime_risk_mapdata_df, geometry='the_geom')

    # Download the crimes chart data.
    cri_chartdata_df = pd.read_gbq("SELECT * FROM justtest.count_crimes")

    # Render the data into the template.
    env = Environment(loader=FileSystemLoader(template_root))
    #overview_template = env.get_template('index2.html')
    neighborhood_template = env.get_template('neighborhood.html')

    # Write the overview.
    #write_overview(gro_mapdata_gdf, neigh_mapdata_gdf, neighborhood_df, overview_template, output_root)

    # Write each of the neighborhood-specific pages.
    neighborhood_df.apply(write_neighborhood, axis=1, args=[
        neighborhood_template, output_root,
        neighborhood_df,
        neigh_mapdata_gdf,
        gro_mapdata_gdf, 
        res_mapdata_gdf,
        bus_mapdata_gdf,
        crime_risk_mapdata_gdf,
        cri_chartdata_df
    ])


# def write_overview(gro_mapdata_gdf, neigh_mapdata_gdf, neighborhood_df, template, output_root):

#     # Render the overview data into a template.
#     output = template.render(
#         # TEMPLATE DATA GOES HERE...
#         gro_mapdata=gro_mapdata_gdf.to_json(),
#         neigh_mapdata=neigh_mapdata_gdf.to_json(),
#         neighborhood_list=neighborhood_df.to_dict('records'),
#     )

#     # Write the report to the local folder.
#     with open(output_root / 'overview.html', 'w') as local_file:
#         local_file.write(output)



def write_neighborhood(neighborhood, template, output_root,
                   neighborhood_df,
                   neigh_mapdata_gdf,
                   gro_mapdata_gdf, 
                   res_mapdata_gdf,
                   bus_mapdata_gdf,
                   crime_risk_mapdata_gdf,
                   cri_chartdata_df):
    import json
    import shapely.geometry
    
    df = neigh_mapdata_gdf
    neigh_mapdata_gdf = df[df.pri_neigh == neighborhood.neighborhood_name]

    df = gro_mapdata_gdf
    gro_mapdata_gdf = df[df.pri_neigh == neighborhood.neighborhood_name]

    df = res_mapdata_gdf
    res_mapdata_gdf = df[df.pri_neigh == neighborhood.neighborhood_name]

    df = bus_mapdata_gdf
    bus_mapdata_gdf = df[df.pri_neigh == neighborhood.neighborhood_name]

    df = crime_risk_mapdata_gdf
    crime_risk_mapdata_gdf = df[df.pri_neigh == neighborhood.neighborhood_name]

    df = cri_chartdata_df
    cri_chartdata_df = df[df.pri_neigh == neighborhood.neighborhood_name]

    # Render the corridor data into a tempate
    output = template.render(
        # TEMPLATE DATA GOES HERE...
        neighborhood=neighborhood.to_dict(),
        gro_mapdata=gro_mapdata_gdf.to_json(),
        res_mapdata=res_mapdata_gdf.to_json(),
        bus_mapdata=bus_mapdata_gdf.to_json(),
        neigh_mapdata=neigh_mapdata_gdf.to_json(),
        crime_risk_mapdata = crime_risk_mapdata_gdf.to_json(),
        cri_chartdata = cri_chartdata_df.to_dict('list'),
    )
    
    with open(output_root / 'neighborhoods' / f'{neighborhood.neighborhood_name}.html', 'w') as local_file:
        local_file.write(output)


if __name__ == '__main__':
    main()
