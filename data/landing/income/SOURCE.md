# ABS Personal Income in Australia

Source: Australian Bureau of Statistics
Release: Personal Income in Australia, 2022-23
Released: 14 November 2025
Reference period: five financial years, 2018-19 to 2022-23
Geography: ASGS Edition 3, 2021 SA2 codes
Downloaded: 2026-09-06
URL: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/latest-release
Licence: Creative Commons Attribution 4.0 International

Compiled from the Linked Employer Employee Dataset, which draws on
administrative data from the Australian taxation system.

## Files, renamed from the ABS originals for path safety

abs_total_income_sa2_2018_19_to_2022_23.xlsx
  Originally "Table 1 - Total income, earners and summary statistics by
  geography, 2018-19 to 2022-23.xlsx". Sheet "Table 1.4" holds the SA2 level
  data. This is the sheet used.

abs_income_distribution_sa2_2022_23.xlsx
  Originally "Table 3 - Total income distribution by geography, 2022-23.xlsx".
  Held for possible later use in deriving an income inequality measure such as
  a percentile ratio. Not used in the current pipeline.

The originals contain spaces and commas, which require quoting on every
command line reference. The renaming is recorded here so the mapping back to
the ABS table numbering is not lost.

## Geographic alignment

The ABS states that in this release the names and boundaries of all SA2s are
based on or concorded to the 2021 edition of ASGS Main Structure. No
correspondence or conversion is required to join against the boundary file.

## Sheet structure

Sheet "Table 1.4" carries a two level header. Row 6 names the metric and row 7
names the financial year, with data from row 10.

The metric blocks are Earners, Median age of earners, Sum, Median and Mean,
each spanning five year columns. Because row 6 is sparse, the blocks are read
by column position rather than by header name.

## Two traps in this file

**Aggregate rows are stacked above the SA2 rows.** Rows for Australia and for
each state appear first, with the state or country name sitting in the SA2 code
column. Footnote rows follow the data at the bottom. Both are removed by
keeping only rows whose first column is exactly nine digits, which avoids
hard coding row positions that would break if the ABS adds a line.

**Values marked "np" are withheld** to protect the confidentiality of
individuals or businesses. Reading these without coercion forces the whole
column to object dtype. They are coerced to missing so they propagate as nulls.

## Income definition

Total income is the sum of employee income, own unincorporated business income,
superannuation, investments and other income. All values are gross pre tax
dollars, nominal and not adjusted for inflation. Government pensions, benefits
and allowances are excluded from the ABS definition, so the figures understate
the resources of areas with a high proportion of pension recipients.

## Coverage and reliability

522 Victorian SA2 rows, matching the boundary file minus the two special
purpose areas. Two further SA2s carry suppressed values, being Alps East and
Lake King, leaving 520 with data.

The ABS excludes SA2s with fewer than 1000 earners from its own published
regional rankings. The same threshold is applied here, which leaves 509
reliable SA2s. The excluded areas are airports, parks and industrial estates
where a handful of earners produce unstable statistics, such as Royal Botanic
Gardens Victoria with three earners.

## Known limitation

Median personal income is a weak proxy for affluence in student dominated
areas. Melbourne CBD North, Melbourne CBD West, Carlton and Clayton North
Notting Hill record the lowest medians in the state yet sustain high rents,
because their residents are largely students supported by family or overseas
funds rather than local earnings.

The reference period also lags the rental listings by roughly three years.
