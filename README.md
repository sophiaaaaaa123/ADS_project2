# ADS Project 2: Real Estate Rental Analysis

## Overview
This project analyses rental listings in Victoria using Domain rental data, spatial accessibility features, and SA2-level demographic and income data.

## Research Questions
1. Which internal and external features are most important for predicting weekly rent?
2. Which suburbs show the highest rental growth potential?
3. Which suburbs are the most affordable and liveable?

## Notebook Order
1. `code/01_external_data.ipynb`
2. `code/02_spatial_features.ipynb`
3. `code/modelling_table.ipynb`
4. `code/04_rental_price_model.ipynb`
5. `code/05_suburb_ranking.ipynb`
6. `code/plant_processing.ipynb`
7. `code/plant_external_validation.ipynb`

## Key Outputs
- `data/curated/master_modelling_table.parquet`
- `data/curated/rental_model_final_test_results.csv`
- `data/curated/rental_model_feature_importance.csv`
- `data/curated/suburb_ranking_top10.csv`
- `plots/rental_model_top20_feature_importance.png`
- `plots/05_suburb_ranking_top10.png`