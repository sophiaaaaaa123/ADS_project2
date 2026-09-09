# ABS SA2 Digital Boundaries

Source: Australian Bureau of Statistics
Product: Australian Statistical Geography Standard (ASGS) Edition 3,
         July 2021 to June 2026
File: SA2_2021_AUST_SHP_GDA2020.zip
Datum: GDA2020, EPSG 7844
Format: ESRI Shapefile
Downloaded: 2026-09-06
URL: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files
Licence: Creative Commons Attribution 4.0 International

## Why Edition 3 and not Edition 4

ASGS Edition 4 was released progressively from July 2026 and splits several
2021 SA2s in high growth areas. It is deliberately not used here, because the
population projection and income datasets in this project are compiled against
2021 SA2 codes.

Mixing editions would cause silent join failures. A property mapped to a 2026
SA2 would find no matching 2021 demographic record, and the result would be a
null rather than an error. This choice is recorded as an assumption in the
analysis.

## Why GDA2020 and not GDA94

GDA2020 became the official national datum in 2017. The two differ by about
1.8 metres on the ground, which is immaterial for most points but can place a
boundary case in the wrong SA2. All project layers are reprojected onto this
datum before any spatial join.

## Contents

2473 SA2 records nationally, of which 524 are in Victoria. The national total
exceeds the published 2472 by one, because the file includes a special purpose
code for Outside Australia.

Two of the 524 Victorian records are special purpose areas with no geographic
extent, being "Migratory - Offshore - Shipping (Vic.)" and "No usual address
(Vic.)". Both have a null AREASQKM21 and appear in no demographic dataset.

## Format note

Shapefile is a multi file format. The .shp, .shx, .dbf and .prj files must all
remain in the same directory. Removing the .prj leaves the layer with no CRS
and every subsequent spatial operation becomes unreliable.

A single file GeoPackage of SA2 alone is not published by the ABS. The only
GeoPackage option bundles every level of the Main Structure into a 505 MB
download, against 48 MB for the SA2 shapefile.
