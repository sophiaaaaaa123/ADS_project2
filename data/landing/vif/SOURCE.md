# Victoria in Future 2023 Projections

Source: Department of Transport and Planning, Victoria
Release: Victoria in Future 2023, Second Release, December 2023
Downloaded: 2026-09-06
URL: https://www.planning.vic.gov.au/guides-and-resources/Data-spatial-and-insights/discover-and-access-planning-open-data/victoria-in-future
Licence: Creative Commons Attribution 4.0 International

The official Victorian state government projection of population and
households. SA2 is the smallest geography for which projections are published.

## Files

VIF2023_SA2_Pop_Hhold_Dwelling_Projections_to_2036_Release_2.xlsx
  The primary source. Sheets used are Total_Population, Total_Dwellings and
  Total_Households.

VIF2023_SA2_Pop_Age_Sex_Projections_to_2036_Release_2.xlsx
  Held for possible later use in deriving an age structure feature, such as the
  share of residents aged 20 to 34 who are more likely to rent than buy. Not
  used in the current pipeline.

## Sheet structure

Each data sheet carries six rows of title and contact information, a blank row,
the real header on row 10, a further blank row, then data from row 12.

Columns are GCCSA, SA4 Code, SA3 Code, "SA2  code", Region Type, Region, then
four year points being 2021, 2026, 2031 and 2036. Intermediate years are not
published.

Note that the SA2 code column name contains two consecutive spaces in the
source file.

## Two traps in this file

**The SA2 code arrives as a float.** Values read as 201011001.0, so converting
straight to string yields "201011001.0" which can never match the ABS boundary
codes. The conversion must pass through int first. The resulting join failure
would be silent rather than raising.

**Five geographic levels are stacked in one sheet.** Region Type takes the
values SA2, SA3, SA4, GCCSA and State. Filtering to SA2 is mandatory, since
retaining any higher level would double count population.

## Coverage

522 SA2 rows, matching the 524 Victorian SA2s in the ABS boundary file minus
the two special purpose areas. The same 522 appear in all three sheets.

## Known characteristic

Eleven SA2s record zero households in 2026, comprising four airports, three
national park areas, two industrial estates and two water or island areas.
Any household based ratio is undefined for these. They are flagged and
excluded rather than imputed, since imputing a value would imply a housing
market that does not exist in these locations.

Dwelling counts appear to be derived from household counts using a fixed
occupancy assumption for most regions, since household growth and dwelling
growth are exactly equal for over half the SA2s. Only a minority, such as
Torquay, Doveton and Frankston, show an independent judgement.
