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
from pipeline_tools import local_file_to_gcs

template_root = Path(__file__).parent / 'templates'
output_root = Path(__file__).parent.parent / 'output'

def main():

    # Download the neighborhood map data.
    neigh_mapdata_df = pd.read_gbq('SELECT * FROM justtest.gro_in_neigh')
    neigh_mapdata_df.neigh_geom = gpd.GeoSeries.from_wkt(neigh_mapdata_df.neigh_geom)
    neigh_mapdata_gdf= gpd.GeoDataFrame(neigh_mapdata_df, geometry='neigh_geom')
    
    # Download the grocery map data.
    gro_mapdata_df = pd.read_gbq("SELECT * FROM justtest.gro_in_neigh")
    gro_mapdata_df.gro_geom = gpd.GeoSeries.from_wkt(gro_mapdata_df.gro_geom)
    gro_mapdata_gdf = gpd.GeoDataFrame(gro_mapdata_df, geometry='gro_geom')  

    # Download the grocery map data.
    res_mapdata_df = pd.read_gbq('SELECT * FROM justtest.gro_in_neigh')
    res_mapdata_df.gro_geom = gpd.GeoSeries.from_wkt(res_mapdata_df.gro_geom)
    res_mapdata_gdf = gpd.GeoDataFrame(res_mapdata_df, geometry='gro_geom')  

    # Download the bus stop map data.
    bus_mapdata_df = pd.read_gbq("SELECT * FROM justtest.bus_in_neigh")
    bus_mapdata_df.stop_geom = gpd.GeoSeries.from_wkt(bus_mapdata_df.stop_geom)
    bus_mapdata_gdf = gpd.GeoDataFrame(bus_mapdata_df, geometry='stop_geom')  

    # Download the neighborhood data.
    neighborhood_df = pd.read_gbq('SELECT * FROM justtest.neighborhood_list')
    nhood_df = pd.read_gbq('SELECT * FROM justtest.nhoods_detail')

    # Download max and min crime data.
    max_crime = pd.read_gbq('SELECT * FROM justtest.max_crime')
    min_crime = pd.read_gbq('SELECT * FROM justtest.min_crime')

    # Download the all crime map data.
    crime_risk_mapdata_df = pd.read_gbq('SELECT * FROM justtest.crime_risk')
    crime_risk_mapdata_df.the_geom = gpd.GeoSeries.from_wkt(crime_risk_mapdata_df.the_geom)
    crime_risk_mapdata_gdf = gpd.GeoDataFrame(crime_risk_mapdata_df, geometry='the_geom')

    # Download the crimes chart data.
    cri_chartdata_df = pd.read_gbq("SELECT * FROM justtest.count_crimes")

    # Download the boundingbox data
    boundingbox_df = pd.read_gbq("SELECT * FROM justtest.boundingbox")

    # Render the data into the template.
    env = Environment(loader=FileSystemLoader(template_root))
    overview_template = env.get_template('index2.html')
    neighborhood_template = env.get_template('neighborhood.html')

    # Download the res_level map data.
    res_level_mapdata_df = pd.read_gbq('SELECT * FROM justtest.res_level')
    res_level_mapdata_df.the_geom = gpd.GeoSeries.from_wkt(res_level_mapdata_df.the_geom)
    res_level_mapdata_gdf = gpd.GeoDataFrame(res_level_mapdata_df, geometry='the_geom')

    # Download the res_level map data.
    gro_level_mapdata_df = pd.read_gbq('SELECT * FROM justtest.gro_level')
    gro_level_mapdata_df.the_geom = gpd.GeoSeries.from_wkt(gro_level_mapdata_df.the_geom)
    gro_level_mapdata_gdf = gpd.GeoDataFrame(gro_level_mapdata_df, geometry='the_geom')

    # Download the res_level map data.
    bus_stop_level_mapdata_df = pd.read_gbq('SELECT * FROM justtest.bus_stop_level')
    bus_stop_level_mapdata_df.the_geom = gpd.GeoSeries.from_wkt(bus_stop_level_mapdata_df.the_geom)
    bus_stop_level_mapdata_gdf = gpd.GeoDataFrame(bus_stop_level_mapdata_df, geometry='the_geom')

    # Download the centroid data
    centroid_df = pd.read_gbq("SELECT * FROM justtest.centroid")


    # Write the overview.
    write_overview(gro_mapdata_gdf, neigh_mapdata_gdf, neighborhood_df, nhood_df, max_crime, min_crime, boundingbox_df, crime_risk_mapdata_gdf,gro_level_mapdata_gdf,bus_stop_level_mapdata_gdf,res_level_mapdata_gdf,overview_template, output_root)

    # Write each of the corridor-specific pages.
    neighborhood_df.apply(write_neighborhood, axis=1, args=[
        neighborhood_template, output_root,
        neighborhood_df,
        neigh_mapdata_gdf,
        gro_mapdata_gdf,
        res_mapdata_gdf,
        bus_mapdata_gdf,
        crime_risk_mapdata_gdf,
        cri_chartdata_df,
        nhood_df,
        centroid_df
    ])


def write_overview(gro_mapdata_gdf, neigh_mapdata_gdf, neighborhood_df, nhood_df, max_crime, min_crime, boundingbox_df, crime_risk_mapdata_gdf,gro_level_mapdata_gdf,bus_stop_level_mapdata_gdf,res_level_mapdata_gdf,template, output_root):

    # Render the overview data into a template.
    output = template.render(
        # TEMPLATE DATA GOES HERE...
        gro_mapdata=gro_mapdata_gdf.to_json(),
        neigh_mapdata=neigh_mapdata_gdf.to_json(),
        neighborhood_list=neighborhood_df.to_dict('records'),
        nhood=nhood_df.to_dict('records'),
        max_crime=max_crime.to_dict('records')[0], 
        min_crime=min_crime.to_dict('records')[0],
        boundingbox = boundingbox_df.to_dict('records'),
        crime_risk_mapdata = crime_risk_mapdata_gdf.to_json(),
        gro_level_mapdata = gro_level_mapdata_gdf.to_json(),
        bus_stop_level_mapdata = bus_stop_level_mapdata_gdf.to_json(),
        res_level_mapdata = res_level_mapdata_gdf.to_json()
    )

    # Write the report to the local folder.
    # with open(output_root / 'index2.html', 'w') as local_file:
    #     local_file.write(output)

    with open(output_root / 'index2.html', 'w') as local_file:
         local_file.write(output)
         local_file_to_gcs(
            local_file_name=local_file.name,
            gcs_bucket_name='shimin_sisun_cloud',
            gcs_blob_name=f'index.html',
            content_type='text/html',
        )



def write_neighborhood(neighborhood, template, output_root,
            neighborhood_df,
            neigh_mapdata_gdf,
            gro_mapdata_gdf, 
            res_mapdata_gdf,
            bus_mapdata_gdf,
            crime_risk_mapdata_gdf,
            cri_chartdata_df,
            nhood_df,
            centroid_df):
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

    df = centroid_df
    centroid_df = df[df.pri_neigh == neighborhood.neighborhood_name]

    # Render the corridor data into a tempate
    output = template.render(
        # TEMPLATE DATA GOES HERE...
        neighborhood=neighborhood.to_dict(),
        neighborhood0=neighborhood_df.to_dict('records')[0],
        gro_mapdata=gro_mapdata_gdf.to_json(),
        res_mapdata=res_mapdata_gdf.to_json(),
        bus_mapdata=bus_mapdata_gdf.to_json(),
        neigh_mapdata=neigh_mapdata_gdf.to_json(),
        crime_risk_mapdata = crime_risk_mapdata_gdf.to_json(),
        cri_chartdata = cri_chartdata_df.to_dict('list'),
        neighborhood_list=neighborhood_df.to_dict('records'),
        nhood=nhood_df.to_dict(),
        centroid = centroid_df.to_dict('list')
    )

    # with open(output_root / 'neighborhood' / f'{neighborhood.neighborhood_name}.html', 'w') as local_file:
    #     local_file.write(output)
    
    with open(output_root / 'neighborhood' / f'{neighborhood.neighborhood_name}.html', 'w') as local_file:
         local_file.write(output)
         local_file_to_gcs(
            local_file_name=local_file.name,
            gcs_bucket_name='shimin_sisun_cloud',
            gcs_blob_name=f"’neighborhood‘/{neighborhood.neighborhood_name}.html",
            content_type='text/html',
        )
    

if __name__ == '__main__':
    main()


