import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

#  Define the ordered scale once
REVIEW_CAT = CategoricalDtype(
    categories=[
        "no_reviews",   # worst / missing
        "low_reviews",
        "medium_reviews",
        "high_reviews",
        "top_reviews",  # best
    ],
    ordered=True,
)

def categorize_reviews(
    df: pd.DataFrame,
    review_columns: list[str],
    *,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Convert numeric review scores into an ordered, categorical scale.

    Categories (worst ➜ best)
    -------------------------
    no_reviews    : NaN / missing
    low_reviews   : score  < 4.0
    medium_reviews: 4.0 ≤ score < 4.6
    high_reviews  : 4.6 ≤ score ≤ 4.8
    top_reviews   : score  > 4.8

    Parameters
    ----------
    df : pd.DataFrame
        Table of listings.
    review_columns : list[str]
        Columns that hold numeric review scores.
    inplace : bool, default False
        • False – work on a deep copy and return it  
        • True  – modify *df* directly (also returned)

    Returns
    -------
    pd.DataFrame
        DataFrame with the chosen review columns recoded as
        ordered-categorical strings.
    """
    if not inplace:
        df = df.copy(deep=True)

    for col in review_columns:
        if col not in df.columns:
            raise KeyError(f"'{col}' not found in the DataFrame.")

        vals = df[col]

        # Vectorised masking + explicit dtype
        df[col] = pd.Categorical(
            np.select(
                [
                    vals.isna(),
                    vals < 4.0,
                    (vals >= 4.0) & (vals < 4.6),
                    (vals >= 4.6) & (vals <= 4.8),
                    vals > 4.8,
                ],
                REVIEW_CAT.categories,   # same order as above
                default="no_reviews",
            ),
            dtype=REVIEW_CAT            # ⚑ sets both categories *and* order
        )

    return df





def convert_and_calculate_days(df, date_column, reference_column):
    """
    Converts a date column to datetime format, calculates the difference (in days)
    from a reference date column, and replaces the original column with the new
    "days_since_{original_name}" column.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame containing the columns.
    - date_column (str): The name of the column to convert and replace.
    - reference_column (str): The column used as a reference for date difference.
    
    Returns:
    - df (pd.DataFrame): Updated DataFrame with renamed column containing days difference.
    """
    # Convert columns to datetime
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df[reference_column] = pd.to_datetime(df[reference_column], errors='coerce')
    
    # Calculate the difference in days
    days_diff = (df[reference_column] - df[date_column]).dt.days
    
    # Create new column name
    new_column_name = f"days_since_{date_column}"
    
    # Drop the original column and add the new one
    df = df.drop(columns=[date_column])
    df[new_column_name] = days_diff
    
    return df


    

def create_first_review_age_categories(df, column_name='days_since_first_review', inplace=False):
    """
    Create ordinal categories for days since first review based on business logic.
    Higher days = more established = better for trust/credibility.
    """
    if not inplace:
        df = df.copy()
    
    # Store the original numeric values
    numeric_values = df[column_name].copy()
    
    def categorize_review_age(days):
        if pd.isna(days):
            return 'no_review_yet'
        elif days <= 30:
            return 'very_new (<= 1 month)'     # Less than 1 month
        elif days <= 180:
            return 'new (<= 6 months)'         # 1-6 months
        elif days <= 365:
            return 'established (<= 1 year)'   # 6 months - 1 year
        elif days <= 1095:
            return 'mature (<= 3 years)'       # 1-3 years
        elif days <= 1825:
            return 'veteran (<= 5 years)'      # 3-5 years
        else:
            return 'legacy (over 5 years)'     # 5+ years
    
    # Apply categorization
    categorical_values = numeric_values.apply(categorize_review_age)
    
    # Create ordered categorical with descriptive names
    categories_order = [
        'no_review_yet',
        'very_new (<= 1 month)',
        'new (<= 6 months)', 
        'established (<= 1 year)', 
        'mature (<= 3 years)', 
        'veteran (<= 5 years)', 
        'legacy (over 5 years)'
    ]
    
    df[column_name] = pd.Categorical(
        categorical_values, 
        categories=categories_order, 
        ordered=True
    )
    
    # Professional output
    print(f"Successfully converted '{column_name}' to categorical")
    print(f"Records processed: {len(df):,} | Missing values handled: {df[column_name].isna().sum()}")
    
    print(f"\nCategory Distribution:")
    print("-" * 60)
    
    # Get counts and percentages
    counts = df[column_name].value_counts().sort_index()
    percentages = df[column_name].value_counts(normalize=True).sort_index() * 100
    
    for category in categories_order:
        if category in counts.index:
            count = counts[category]
            pct = percentages[category]
            print(f"{category:<35} {count:>8,} {pct:>6.1f}%")
        else:
            print(f"{category:<35} {0:>8,} {0:>6.1f}%")
    
    print("-" * 60)
    print(f"{'Total':<35} {len(df):>8,} {'100.0%':>6}")
    
    return df




def create_last_review_recency_categories(df, column_name='days_since_last_review', inplace=False):
    """
    Create ordinal categories for days since last review based on recency/freshness.
    """
    if not inplace:
        df = df.copy()
    
    
    # Store the original numeric values
    numeric_values = df[column_name].copy()
    
    def categorize_last_review_recency(days):
        if pd.isna(days):
            return 'no_review'
        elif days <= 7:
            return 'very_recent (<= 1 week)'    # Within a week - very active
        elif days <= 30:
            return 'recent (<= 1 month)'         # Within a month - active
        elif days <= 90:
            return 'somewhat_recent (<= 3 months)' # Within 3 months - moderately active
        elif days <= 180:
            return 'old (<= 6 months)'            # 3-6 months - getting stale
        elif days <= 365:
            return 'very_old (<= 1 year)'       # 6 months - 1 year - quite stale
        else:
            return 'dormant (over a year)'        # Over 1 year - potentially inactive
    
    # Apply categorization
    categorical_values = numeric_values.apply(categorize_last_review_recency)
    
    # Create ordered categorical with the FULL descriptive names
    categories_order = [
        'no_review', 
        'very_recent (<= 1 week)', 
        'recent (<= 1 month)', 
        'somewhat_recent (<= 3 months)', 
        'old (<= 6 months)', 
        'very_old (<= 1 year)', 
        'dormant (over a year)'
    ]
    
    df[column_name] = pd.Categorical(
        categorical_values, 
        categories=categories_order, 
        ordered=True
    )
    
    
    print(f"Successfully converted '{column_name}' to categorical")
    print(f"Records processed: {len(df):,} | Missing values now: {df[column_name].isna().sum()}")
    
    print(f"\nCategory Distribution:")
    print("-" * 55)
    
    counts = df[column_name].value_counts().sort_index()
    percentages = df[column_name].value_counts(normalize=True).sort_index() * 100
    
    for category in categories_order:
        if category in counts.index:
            count = counts[category]
            pct = percentages[category]
            print(f"{category:<35} {count:>8,} {pct:>6.1f}%")
    
    print("-" * 55)
    print(f"{'Total':<35} {len(df):>8,} {'100.0%':>6}")
    
    return df


def convert_to_ordered_category(df, column_name, category_order):
    """
    Converts a specified column in a DataFrame to an ordered categorical variable.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the column.
    - column_name (str): The column to convert.
    - category_order (list): List of ordered category values.

    Returns:
    - df (pd.DataFrame): Updated DataFrame with the ordered categorical column.
    """
    df[column_name] = pd.Categorical(df[column_name], categories=category_order, ordered=True)
    return df

def convert_columns_to_boolean(df, columns):
    """
    Converts specified columns to boolean type.
    - If values are 0/1, they are cast using `astype(bool)`
    - If values are 't'/'f', they are mapped to True/False

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the columns.
    - columns (list): List of column names to convert.

    Returns:
    - df (pd.DataFrame): Updated DataFrame with boolean columns.
    """
    for col in columns:
        unique_vals = df[col].dropna().unique()

        if set(unique_vals).issubset({0, 1}):
            df[col] = df[col].astype(bool)
        elif set(unique_vals).issubset({'t', 'f'}):
            df[col] = df[col].map({'t': True, 'f': False})
        else:
            raise ValueError(f"Column '{col}' contains unsupported values for boolean conversion.")

    return df