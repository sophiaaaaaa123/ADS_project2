# Victorian School Locations

Source: Department of Education, Victoria, via data.vic.gov.au
Dataset: School Locations 2024
File: dv378_DataVic-SchoolLocations-2024.csv
Downloaded: 2026-09-07
URL: https://discover.data.vic.gov.au/dataset/school-locations-2024
Licence: Creative Commons Attribution 4.0 International

2294 school campuses across Victoria, government and non government, primary
and secondary. Collected as part of the ongoing registration of schools.

## Coordinates

X is longitude and Y is latitude, in WGS84 decimal degrees, following the
usual GIS convention. The notebook renames them on read so that the pair can
never be transposed later.

Observed ranges are 141.08 to 149.75 for longitude and -38.75 to -34.17 for
latitude, both consistent with the extent of Victoria.

## Encoding

The file is cp1252, not UTF-8. School names such as St Mary's College use the
Windows curly apostrophe, which raises a UnicodeDecodeError under the default
encoding. Read it with encoding="cp1252".

## Known characteristics

One school, St Ignatius College Geelong at Drysdale, has no coordinates in the
source and is excluded, leaving 2293 usable records.

School_No is not unique. The 2294 rows carry only 2154 distinct values, because
some schools operate several campuses and each campus is recorded as a separate
row. This is correct for a nearest school distance, since every campus is a
real location, but it means a row count is a campus count rather than a school
count.

## Field values

Education_Sector: Government 1570, Catholic 494, Independent 229.

School_Type: Primary 1570, Secondary 356, Pri/Sec 249, Special 114,
Language 4.

Pri/Sec campuses serve both stages and are counted towards both the primary
and the secondary totals in sa2_features.parquet, so those two counts overlap
and do not sum to the total.

## Spatial assignment

All 2293 schools with coordinates matched to a Victorian SA2 by point in
polygon against the 2021 boundaries, with none falling outside. This dataset
served as the first validation of the spatial join pipeline later applied to
property coordinates.
