# OpenStreetMap Green Space and Retail

Source: OpenStreetMap contributors, via the Overpass API
Endpoint: https://overpass-api.de/api/interpreter
Queried: 2026-09-07
Licence: Open Database License (ODbL). Attribution to OpenStreetMap
contributors is required in any published output.

## Files

osm_parks_vic.json
  Raw Overpass response for leisure=park across Victoria. 17005 elements,
  16765 ways and 240 relations.

osm_malls_vic.json
  Raw Overpass response for shop=mall across Victoria. 433 elements, of which
  383 fall inside the state boundary.

## Why the raw responses are saved

Overpass returns whatever OpenStreetMap contains at the moment of the request.
Querying it live on every notebook run would make the analysis
unreproducible, since the same code would return different features weeks
later as contributors edit the map. The notebook reads these files and only
contacts Overpass if a file is missing.

## Request requirement

The public Overpass instance is fronted by Apache, which rejects the default
Python requests user agent with a 406 before the query reaches Overpass at
all. A descriptive User-Agent header is required. This is also the courtesy
the Overpass operators ask for, since it lets them contact a heavy user rather
than simply blocking them.

## Query design

Only a representative coordinate is requested, using "out center", rather than
the full polygon geometry. Full geometry multiplies the response size by about
two orders of magnitude and is not needed for a nearest neighbour or radius
calculation.

The bounding box is rectangular and therefore captures parts of New South
Wales and the Australian Capital Territory along the northern and eastern
edges. Calwell Shopping Centre in Canberra is one such record. Points are
filtered against the SA2 boundaries rather than by tightening the box, which
would risk clipping genuine Victorian features near the border. 50 shopping
centres were excluded this way.

## Known limitations

**No area is available.** Computing true park area would require the full
polygon geometry. A named park is used as a proxy for a significant one, on
the basis that a named park in OpenStreetMap is generally a formally managed
public space, whereas unnamed leisure=park polygons are typically verges,
median strips and pocket gardens. 8042 of the 17005 records carry a name. The
operator tag supports this reading, with Manningham City Council, Maroondah
City Council, City of Casey and Parks Victoria appearing most often.

**Radius counts slightly overstate the number of distinct parks.** A linear
reserve such as Melbourne Water Pipe Reserve is mapped as 32 adjacent ways,
each counted separately.

**Deduplicating parks by name would be wrong.** Apex Park appears 46 times and
Lions Park 33 times, but these are separate parks in different towns, built by
the same service clubs, not one fragmented park. Of 8042 named records, 1286
share a name with another, and the great majority of those are genuinely
distinct places. The overstatement from fragmentation is left uncorrected and
recorded here instead.

**shop=mall is applied loosely in OpenStreetMap.** Some records are individual
shops rather than shopping centres, such as John Thomson & Co in western
Victoria. The derived feature is therefore better read as distance to the
nearest retail cluster than as distance to a major shopping centre.
