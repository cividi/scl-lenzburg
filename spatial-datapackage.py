import json
import pandas as pd
import geopandas as gpd

import pyproj
from shapely import wkt
from shapely.geometry import Point
from shapely.ops import transform

import shapely.speedups
shapely.speedups.enable()

dp_name = "space-syntax-snapshot"
crs_from = "epsg:2056"
crs_to = "epsg:4326"
crop_ctr_pt = Point(8.17116,47.39098)
crop_radius = 5000

crop = transform(pyproj.Transformer.from_crs(pyproj.CRS(crs_to), pyproj.CRS(crs_from), always_xy=True).transform, crop_ctr_pt).buffer(crop_radius)

with open('data/'+dp_name+'/datapackage.json') as f:
    data = json.load(f)

    r_ = []

    r_.append({
        "name": "mapbox-background",
        "mediatype": "application/vnd.mapbox-vector-tile",
        "path": "mapbox://styles/gemeindescan/ck6rp249516tg1iqkmt48o4pz"
    })

    for r in data["resources"]:
        gdf = pd.read_csv('data/' + dp_name + '/' + r["path"])
        gdf['geometry'] = gdf['geom_wkt'].apply(wkt.loads)
        gdf = gdf.drop(columns=["geom_wkt"])
        gdf = gpd.GeoDataFrame(gdf, crs=crs_from)
        
        crop_mask = gdf.intersects(crop)
        gdf = gdf.loc[crop_mask]
        gdf = gdf.loc[gdf["class"] != 'rm']

        gdf = gdf.to_crs(crs_to)

        gdf.to_file("exports/snapshots/"+dp_name+".geojson", driver="GeoJSON")

        r_.append({
            "name": r["name"],
            "mediatype": "application/geo+json",
            "data": json.loads(gdf.to_json()),
        })
    
    view_r = []
    for r in r_:
        view_r.append(r["name"])

    data["resources"] = r_
    data["views"][0]["resources"] = view_r

    with open('exports/snapshots/'+dp_name+'.json', 'w') as json_file:
        json.dump(data, json_file)