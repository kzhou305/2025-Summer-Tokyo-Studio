# INSTRUCTIONS - To run in terminal, match the name of this file.
## exec(open("C:/Users/user/clip_GPS_to_boundary.py").read())
# ^^^^^^^
import os
from pathlib import Path
import pandas as pd
# pip install geopandas
import geopandas as gpd
from shapely.geometry import Point

# Change the paths to your local folders, as needed.
input_folder = Path("C:/Users/user/GPSDatafolder")
output_folder = Path("C:/Users/user/ShareFolder")
output_folder.mkdir(parents=True, exist_ok=True)
# Change boundary_path to a different polygon boundary, as needed.
boundary_path = Path("C:/Users/user/data/yourboundary.shp")
# read
boundary = gpd.read_file(boundary_path).to_crs("EPSG:4326")


for file_name in os.listdir(input_folder):
    if file_name.startswith("GT_") and file_name.endswith(".csv"):
        input_path = os.path.join(input_folder, file_name)

        df = pd.read_csv(input_path)

        if 'lon' in df.columns and 'lat' in df.columns:
            geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]

            # Convert to geodataframe
            gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
            
            clipped = gpd.clip(gdf, boundary)

            # save
            output_file = f"clipped_{file_name}"
            ##output_path = os.path.join(output_folder, output_file)
            output_path = output_folder / output_file

            # overwrite
            if output_path.exists():
                output_path.unlink()

            clipped.drop(columns='geometry').to_csv(output_path, index=False)

            print(f"Saved the clipped CSV: {output_path}")
        else:
            print(f"Skipped {file_name}: missing 'lon' or 'lat' columns.")
