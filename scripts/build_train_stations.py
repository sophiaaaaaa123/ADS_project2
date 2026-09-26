"""Rebuild the station input using the original external-data notebook rules."""

import io
import os
from pathlib import Path
import sys
import zipfile

for name, folder in (("PROJ_LIB", "proj"), ("GDAL_DATA", "gdal")):
    for base in (Path(sys.prefix) / "Library" / "share", Path(sys.prefix) / "share"):
        if (base / folder).exists():
            os.environ.setdefault(name, str(base / folder))
            break

import geopandas as gpd
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    archive = root / "data/landing/ptv/gtfs.zip"
    frames = []
    with zipfile.ZipFile(archive) as outer:
        for branch, network in (("1", "regional"), ("2", "metropolitan")):
            matches = [
                name for name in outer.namelist()
                if name.endswith("google_transit.zip")
                and name.split("/")[-2] == branch
            ]
            assert len(matches) == 1, f"Unexpected archives for branch {branch}"
            with zipfile.ZipFile(io.BytesIO(outer.read(matches[0]))) as inner:
                stops = pd.read_csv(inner.open("stops.txt"))
            stations = stops.loc[
                stops["location_type"].eq(1),
                ["stop_id", "stop_name", "stop_lat", "stop_lon"],
            ].copy()
            stations["network"] = network
            frames.append(stations)
            print(f"{network}: {len(stations)} station records")

    stations = pd.concat(frames, ignore_index=True).rename(
        columns={"stop_lat": "latitude", "stop_lon": "longitude"}
    )
    assert stations[["stop_id", "latitude", "longitude"]].notna().all().all()
    consistency = stations.groupby("stop_id")[["latitude", "longitude"]].nunique()
    assert consistency.le(1).all().all(), "Conflicting coordinates for a stop_id"
    both = stations.loc[stations["stop_id"].duplicated(keep=False), "stop_id"]
    stations = stations.drop_duplicates("stop_id", keep="first").reset_index(drop=True)
    stations["serves_both_networks"] = stations["stop_id"].isin(both)
    assert stations["latitude"].between(-39.2, -33.9).all()
    assert stations["longitude"].between(140.9, 150.1).all()

    sa2 = gpd.read_file(root / "data/raw/sa2_features.gpkg")
    points = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),
        crs="EPSG:4326",
    ).to_crs(sa2.crs)
    joined = gpd.sjoin(
        points, sa2[["sa2_code_2021", "sa2_name_2021", "geometry"]],
        how="left", predicate="within",
    )
    assert len(joined) == len(stations), "Spatial join duplicated station rows"
    result = pd.DataFrame(joined.drop(columns=["geometry", "index_right"]))
    result["in_victoria"] = result["sa2_code_2021"].notna()
    assert result["stop_id"].is_unique
    assert len(result) == 320, "Station count differs from the training pipeline"
    output = root / "data/curated/vic_train_stations.parquet"
    result.to_parquet(output, index=False)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), pd.read_parquet(output))
    print(f"Saved and verified {len(result)} stations: {output}")
    print(f"Both networks: {result['serves_both_networks'].sum()}")
    print(f"Inside Victoria: {result['in_victoria'].sum()}")
    print("Outside Victoria (retained for proximity):")
    print(result.loc[~result["in_victoria"], ["stop_id", "stop_name"]].to_string(index=False))


if __name__ == "__main__":
    main()
