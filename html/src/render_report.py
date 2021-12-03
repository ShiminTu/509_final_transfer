#####
# Setting environment variable. NOTE: This is not a production-safe practice.
# This is only acceptable because this is a lab.
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/tushimin/Desktop/musa-509-final-27b36afe08d2.json'
#####

import geopandas as gpd
import pandas as pd
from pathlib import Path
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

    # Download the chart data.

    # Download the population density list data.

    # Render the data into the template.
    env = Environment(loader=FileSystemLoader(template_root))
    template = env.get_template('index2.html')
    output = template.render(
        # TEMPLATE DATA GOES HERE...
        res_mapdata=res_mapdata_gdf.to_json(),
        neigh_mapdata=neigh_mapdata_gdf.to_json(),
    )

    # Save the rendered output to a file in the "output" folder.
    with open(output_root / 'index2.html', mode='w') as outfile:
        outfile.write(output)

if __name__ == '__main__':
    main()

