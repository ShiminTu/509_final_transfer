#####
# Setting environment variable. NOTE: This is not a production-safe practice.
# This is only acceptable because this is a lab.
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/CSS/Desktop/musa-509-final-27b36afe08d2.json'
#####
import geopandas as gpd
import pandas as pd
from pathlib import Path
from tempfile import NamedTemporaryFile
from jinja2 import Environment, FileSystemLoader


template_root = Path(__file__).parent / 'templates'
output_root = Path(__file__).parent.parent / 'output'

def main():

    # Download the neighborhood map data.
    neigh_mapdata_df = pd.read_gbq('SELECT * FROM justtest.gro_in_neigh')
    neigh_mapdata_df.neigh_geom = gpd.GeoSeries.from_wkt(neigh_mapdata_df.neigh_geom)
    neigh_mapdata_gdf= gpd.GeoDataFrame(neigh_mapdata_df, geometry='neigh_geom')
    

    # Download the grocery map data.
    res_mapdata_df = pd.read_gbq('SELECT * FROM justtest.gro_in_neigh')
    res_mapdata_df.gro_geom = gpd.GeoSeries.from_wkt(res_mapdata_df.gro_geom)
    res_mapdata_gdf = gpd.GeoDataFrame(res_mapdata_df, geometry='gro_geom')  

    # Download the neighborhood list data.
    neighborhood_df =pd.read_gbq('SELECT * FROM justtest.neighborhood_list')

     # Render the data into the template.
    env = Environment(loader=FileSystemLoader(template_root))
    overview_template = env.get_template('index2.html')
    neighborhood_template = env.get_template('neighborhood.html')


    # Write the overview.
    write_overview(res_mapdata_gdf, neigh_mapdata_gdf, neighborhood_df, overview_template, output_root)

    # Write each of the corridor-specific pages.
    neighborhood_df.apply(write_corridor, axis=1, args=[
        neighborhood_template, output_root,
        neighborhood_df,
        res_mapdata_gdf, 
        neigh_mapdata_gdf,
    ])


def write_overview(res_mapdata_gdf, neigh_mapdata_gdf, neighborhood_df, template, output_root):

    # Render the overview data into a template.
    output = template.render(
        # TEMPLATE DATA GOES HERE...
        res_mapdata=res_mapdata_gdf.to_json(),
        neigh_mapdata=neigh_mapdata_gdf.to_json(),
        neighborhood_list=neighborhood_df.to_dict('records'),
    )

    # Write the report to the local folder.
    with open(output_root / 'index2.html', 'w') as local_file:
        local_file.write(output)



def write_corridor(neighborhood, template, output_root,
                   neighborhood_df,
                   res_mapdata_gdf, 
                   neigh_mapdata_gdf,):
    import json
    import shapely.geometry

    # Render the corridor data into a tempate
    output = template.render(
        # TEMPLATE DATA GOES HERE...
        res_mapdata=res_mapdata_gdf.to_json(),
        neigh_mapdata=neigh_mapdata_gdf.to_json(),
        neighborhood_list=neighborhood_df.to_dict('records'),
    )

    with open(output_root / 'neighborhood.html', 'w') as local_file:
        local_file.write(output)


if __name__ == '__main__':
    main()
