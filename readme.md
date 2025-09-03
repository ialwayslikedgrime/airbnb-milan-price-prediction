
## Exploratory Data Analysis (EDA)

Below is the median price per person by neighborhood in Milan (room type: Entire home/apt):

![Median price per person by neighborhood](figures/median_price_per_person_Entire_home_apt.png)




# Dataset Overview

As an initial step, we load the datasets. Multiple datasets were downloaded from Inside Airbnb, including:

1. **Listings Data**
   * `listings_summary.csv`: Summarized listing information
   * `listings_extended.csv`: Detailed listing information

2. **Calendar Data**
   * `calendar.csv`: Daily availability and pricing data

3. **Neighborhood Data**
   * `neighbourhoods.csv`: Tabular neighborhood information
   * `neighbourhoods.geojson`: Geospatial neighborhood boundaries

4. **Reviews Data**
   * `reviews.csv`: Detailed review information
   * `reviews_id_date.csv`: Review IDs and dates only

To understand the structure of these datasets, we first examined their size and shape. Through this comparison, we discovered that `listings_summary.csv` is a subset of `listings_extended.csv`, and `reviews_id_date.csv` is a subset of `reviews.csv`.

Based on these findings, we proceeded with the following datasets:

## Summary of Retained Datasets

After reviewing the available datasets, we retained the following files for analysis:

### 1. Listings Data
- **df_listings_extended** (from `listings_extended.csv`)  
  Contains comprehensive information about Airbnb listings, including host details, pricing, amenities, and availability.

### 2. Reviews Data
- **df_reviews** (from `reviews.csv`)  
  Contains guest reviews with review dates, reviewer details, and comments.

### 3. Calendar Data
- **df_calendar** (from `calendar.csv`)  
  Provides daily availability and pricing information for each listing.

### 4. Neighborhood Data
- **df_neighborhoods** (from `neighbourhoods.csv`)  
  Contains neighborhood names and classifications.
- **gdf_neighborhoods** (from `neighbourhoods.geojson`)  
  Contains geospatial boundaries of neighborhoods for mapping and spatial analysis.

### Final Decision
The `listings_summary.csv` and `reviews_id_date.csv` files were excluded as they contained redundant information. The retained datasets can be merged using `listing_id` and `neighbourhood` as key fields.
