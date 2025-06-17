import os
import pandas as pd
from pathlib import Path

input_folder = Path("C:/Users//user/GPSDataFolder")
output_folder = Path("C:/Users/user/shareFolder")
output_folder.mkdir(parents=True, exist_ok=True)

summary_path = output_folder / "summary_unique_tripid.csv"

overwrite = True
if overwrite and summary_path.exists():
    summary_path.unlink()
    print(f"Deleted existing summary file at {summary_path} to allow overwrite.")

all_summaries = []

# Loop through GPS files
for file_name in os.listdir(input_folder):
    if file_name.startswith("GT_") and file_name.endswith(".csv"):
        input_path = input_folder / file_name
        print(f"Processing {file_name}...")

        gps_df = pd.read_csv(input_path)

        if not {'tripid', 'transportmode'}.issubset(gps_df.columns):
            print(f"Skipping {file_name} - missing required columns.")
            continue

        gps_df = gps_df.dropna(subset=['tripid', 'transportmode'])

        # Count unique trip IDs overall
        num_unique_tripids = gps_df['tripid'].nunique()

        # Count unique tripid per transportmode
        mode_tripid_counts = (
            gps_df.groupby('transportmode')['tripid']
            .nunique()
            .to_dict()
        )

        summary = {'file_name': file_name, 'num_unique_tripids': num_unique_tripids}
        for mode, count in mode_tripid_counts.items():
            summary[f'uq_{mode}'] = count

        all_summaries.append(summary)


summary_df = pd.DataFrame(all_summaries).fillna(0)

# Save
summary_df.to_csv(summary_path, index=False)
print(f"\nSaved summary to {summary_path}")
