# Victoria Rental Data Preprocessing

## Overview

This preprocessing pipeline cleans and prepares the Victoria rental listing dataset for subsequent exploratory analysis and modelling.

The raw dataset contains rental listings collected from Domain.com.au, including rental prices, property characteristics, location information, listing information, agency details, and structured property features.

The preprocessing was conducted using PySpark. The final data are separated into:

- `analysis_data`: cleaned variables intended for subsequent analysis and modelling.
- `metadata`: supplementary listing information that can be linked back to the analysis data using `listing_id`.

---

## Input Data

The raw rental data are read from:

```text
domain/Data/vic_rentals_all.csv
```

The original dataset contains **12,738 observations**.

---

## Preprocessing Steps

### 1. Filter listings to 2025

Only listings with `date_listed` in 2025 were retained to ensure that the analysis uses a consistent time period.

After filtering:

- Original observations: 12,738
- 2025 observations: 12,064

---

### 2. Clean available date

The original `available_date` variable was stored as a string containing the weekday, for example:

```text
Tuesday, 02 September 2025
```

The weekday prefix was removed and the remaining value was converted to a Spark date using the format:

```text
dd MMMM yyyy
```

Two variables were created:

- `available_date_clean`: cleaned date variable.
- `available_weekday`: weekday derived from the cleaned available date.

The original `available_date` was retained for reference.

---

### 3. Investigate missing values

Missing values were examined across all variables before further preprocessing.

Two variables contained excessive missingness and were removed:

- `land_area`: approximately 99.98% missing.
- `property_id`: approximately 82.11% missing and primarily an identifier.

Other variables with missing values were retained and handled individually where appropriate.

---

### 4. Clean weekly rent

`weekly_rent` was initially stored as a string. All non-missing values were checked and confirmed to be numeric before the variable was converted to `double`.

Listings with missing or non-positive weekly rent were removed.

Three listings contained implausibly high weekly rents between approximately $315,000 and $808,500 per week. Manual inspection showed that their bond amounts and other property information were inconsistent with these values, indicating likely data extraction errors.

These three records were removed:

```text
17747509
17697966
17750082
```

Other high weekly rents were retained because they may represent genuine high-value or luxury rental properties.

---

### 5. Check duplicate records

Duplicates were checked using both:

- duplicated `listing_id` values;
- completely duplicated rows.

No duplicated listing IDs or completely duplicated observations were identified.

---

### 6. Restrict property types

The distribution of `primary_type` was examined and the analysis was restricted to the four main residential rental categories:

- `House`
- `Apartment`
- `Townhouse/Villa`
- `New Developments`

Categories such as `Any` and `Land` were excluded because they did not represent the main residential rental property groups used for subsequent analysis.

---

### 7. Clean bond values

The relationship and distribution of `bond` and `weekly_rent` were examined.

One implausible bond value was identified:

```text
listing_id: 17591648
weekly_rent: $490
bond: $212,917
```

The listing itself was retained, but the invalid bond value was replaced with a missing value.

After correcting this value, the correlation between `bond` and `weekly_rent` increased from approximately **0.5778 to 0.9311**, while the standard deviation of bond decreased substantially.

---

### 8. Investigate bond imputation

Model-based imputation was investigated for missing bond values.

Three regression approaches were compared using an 80/20 train-test split:

- Linear Regression
- Random Forest
- Gradient-Boosted Trees (GBT)

`weekly_rent` was deliberately excluded from the predictors because it is the downstream prediction target. Using weekly rent to impute bond would introduce target leakage.

The available predictors included property type and other listing characteristics.

All three models showed poor predictive performance. Random Forest performed best but achieved only approximately:

```text
R² = 0.075
MAE = $788.88
```

This indicated that the available predictors could not reliably estimate missing bond values. Therefore, model-based imputation was not used.

---

### 9. Impute missing bond values

Missing bond values were instead imputed using the median bond within each `primary_type`.

The group medians were:

| Primary type | Median bond ($) |
| --- | ---: |
| Apartment | 2,390 |
| House | 2,390 |
| Townhouse/Villa | 2,824 |
| New Developments | 1,955 |

A total of **653 bond values** were imputed.

A binary variable, `bond_imputed`, was created to identify whether the bond value for an observation was imputed:

```text
0 = original observed bond
1 = imputed bond
```

---

### 10. Clean bedrooms and bathrooms

Missing bedroom and bathroom values were investigated by property type.

A substantial proportion of missing bedroom values occurred among `Studio` properties. Because studios do not contain a separate bedroom, missing `bedrooms` values for Studio listings were set to:

```text
bedrooms = 0
```

After this adjustment, only **28 observations**, approximately **0.23%** of the data, had remaining missing values in `bedrooms` and/or `bathrooms`.

Because this represented a very small proportion of the dataset and these variables are important property characteristics, the remaining observations were removed rather than imputed.

---

### 11. Clean and impute carspaces

Missing `carspaces` values varied substantially across property types.

The observed distributions showed that:

- Apartments typically had 1 carspace.
- Houses typically had 2 carspaces.
- Townhouses/Villas typically had 2 carspaces.

Missing values were therefore imputed using these group-specific typical values:

| Primary type | Imputed carspaces |
| --- | ---: |
| Apartment | 1 |
| House | 2 |
| Townhouse/Villa | 2 |

All `New Developments` listings had missing carspace information and were classified as `New Apartments / Off the Plan`. Because there were no observed carspace values within this group, no group-specific typical value could be estimated.

Their missing `carspaces` values were conservatively set to:

```text
carspaces = 0
```

Here, 0 represents no recorded carspace information rather than confirmation that the property physically has no parking space.

A binary variable, `carspaces_imputed`, was retained:

```text
0 = original observed carspaces
1 = imputed carspaces
```

---

### 12. Handle remaining missing analysis values

After the previous cleaning and imputation steps, the remaining missing values were concentrated in supplementary metadata variables and geographic coordinates.

Only **3 observations** had missing `lat` and `lon` among the variables required for subsequent analysis.

Because these observations represented approximately **0.03%** of the dataset, they were removed rather than imputing geographic coordinates.

Missing values in fields such as `structured_features`, `agent_names`, `address`, `url`, and agency information were not used as a reason to remove observations because these variables were separated into the metadata dataset.

---

## Final Datasets

The cleaned data were separated into two datasets.

Both datasets retain `listing_id`, which acts as the key for linking them when required.

### Analysis Data

`analysis_data` contains the cleaned variables intended for subsequent analysis and modelling.

Variables include:

- `listing_id`
- `suburb`
- `postcode`
- `lat`
- `lon`
- `weekly_rent`
- `bond`
- `available_date`
- `date_listed`
- `days_listed`
- `bedrooms`
- `bathrooms`
- `carspaces`
- `scraped_date`
- `photo_count`
- `video_count`
- `floorplans_count`
- `virtual_tour`
- `property_type`
- `primary_type`
- `secondary_type`
- `available_date_clean`
- `available_weekday`
- `bond_imputed`
- `carspaces_imputed`

Final dimensions:

```text
Rows: 11,945
Columns: 25
```

A final missing-value check confirmed that all 25 analysis variables contain **0 missing values**.

The dataset is saved in Parquet format at:

```text
data/analysis_data
```

---

### Metadata

`metadata` contains supplementary listing information that is not included directly in the main analysis dataset.

Variables include:

- `listing_id`
- `address`
- `url`
- `domain_page_id`
- `agent_names`
- `agency`
- `agency_id`
- `structured_features`

The metadata are saved in Parquet format at:

```text
data/metadata
```

Missing values may remain in the metadata because these fields are supplementary and are not required for the main analysis dataset.

---

## Linking Analysis Data and Metadata

The two datasets can be connected using `listing_id`.

For example:

```python
analysis_data = spark.read.parquet("data/analysis_data")
metadata = spark.read.parquet("data/metadata")

full_data = analysis_data.join(
    metadata,
    on="listing_id",
    how="left"
)
```

A left join is recommended when adding metadata to the analysis dataset because it preserves all observations in `analysis_data`.

---

## Output Structure

The processed data are stored as:

```text
data/
├── analysis_data/
└── metadata/
```

The use of Parquet preserves Spark data types and allows the processed datasets to be loaded directly for subsequent analysis without repeating the preprocessing pipeline.

---

## Reproducing the Preprocessing

Run:

```text
preprocessing.ipynb
```

from the project root directory.

The notebook:

1. reads the raw rental data;
2. restricts listings to 2025;
3. cleans date variables;
4. investigates and handles missing values;
5. cleans weekly rent and removes invalid observations;
6. checks duplicate records;
7. restricts the analysis to relevant residential property types;
8. cleans and imputes bond values;
9. cleans bedroom and bathroom values;
10. imputes missing carspace values;
11. removes the remaining observations with missing analysis variables;
12. creates and saves the final `analysis_data` and `metadata` datasets.

The resulting Parquet datasets can then be used directly for subsequent exploratory analysis and modelling.