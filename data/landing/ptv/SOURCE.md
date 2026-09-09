# PTV GTFS Schedule

Source: Department of Transport and Planning, Victoria
Dataset: GTFS Schedule
Downloaded: 2026-09-07
URL: https://opendata.transport.vic.gov.au/dataset/gtfs-schedule
Licence: Creative Commons Attribution 4.0 International

## Do not unpack this archive

gtfs.zip holds one entry per operational branch at its root, named
"1/google_transit.zip" and so on. Unpacking adds a "gtfs" folder on top, so a
path written against the unpacked layout fails against the archive itself.
The notebook reads the archive directly through a helper that locates the
inner archives by search rather than by a hard coded path.

Unpacking also writes over three hundred megabytes of timetable data that this
project never reads, since only stops.txt from two of the eight branches is
used.

## Branch identification

agency.txt names every branch "Transport Victoria", so the mode was determined
from route_type in routes.txt instead:

  Branch 1   Rail        111 stations   regional, V/Line
  Branch 2   type 400    226 stations   suburban, Metro
  Branch 10  type 102     10 stations   long distance interstate
  Branch 3   Tram          0 stations
  Branch 4, 5, 6, 11  Bus  0 stations

Only branches 1 and 2 are used.

Trams and buses are excluded deliberately. Melbourne tram stops sit every few
hundred metres, so including them would make a nearest stop distance feature
almost constant across the inner suburbs and destroy its signal. Branch 10 is
long distance interstate rail running once or twice a day, which is irrelevant
to commuting and overlaps the regional network.

## Station extraction

stops.txt includes individual platforms, entrances and bus replacement points
alongside the stations themselves. Only records with location_type equal to 1
are stations. Without this filter a station such as Flinders Street appears
many times and any nearest station calculation is meaningless. Branch 2 holds
2859 stop records for only 226 stations.

Only the rail branches carry location_type 1 records at all, because trams and
buses have no multi platform structure requiring in station navigation.

## Deduplication

34 station names appear in both branches. Each shares an identical stop_id and
identical coordinates, since PTV publishes the same station record in both
branch archives. Deduplicating on stop_id is therefore lossless, and this is
verified in the notebook by checking that no stop_id carries more than one
distinct coordinate pair.

17 stations remain flagged as serving both networks, which indicates better
connectivity than a suburban only station.

## Records outside Victoria

Albury station lies in New South Wales, a few kilometres north of the border,
and is the terminus of the V/Line Albury line. It correctly matches no
Victorian SA2 and is flagged rather than dropped, because for properties near
Wodonga it may genuinely be the nearest station.
