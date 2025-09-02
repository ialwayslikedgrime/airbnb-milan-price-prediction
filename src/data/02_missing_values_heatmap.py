import pandas as pd
from typing import List

def compute_missing_corr(
    df: pd.DataFrame,
    missing_columns: List[str],
    indicator_col: str = "number_of_reviews"
) -> pd.DataFrame:
    """
    Compute the Pearson correlation matrix between:
    - a binary mask representing missing values in the specified columns, and
    - a binary flag equal to 1 when `indicator_col` is 0 and 0 otherwise.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to analyze.
    missing_columns : list[str]
        Columns to include when constructing the missing-value mask.
    indicator_col : str, default "number_of_reviews"
        Numeric column used to create the 0-vs-other flag.

    Returns
    -------
    pd.DataFrame
        Correlation matrix combining the missing-value mask and the
        `{indicator_col}_0_vs_other` binary flag.

    Raises
    ------
    ValueError
        If none of the requested `missing_columns` are found in `df`.
    """
    # Keep only columns present in the DataFrame
    valid_missing_cols = [c for c in missing_columns if c in df.columns]
    if not valid_missing_cols:
        raise ValueError("None of the specified columns are present in the DataFrame.")

    # Create the 0-vs-other binary flag
    binary_flag_name = f"{indicator_col}_0_vs_other"
    df = df.copy()  # prevent side effects on the original DataFrame
    df[binary_flag_name] = (df[indicator_col] == 0).astype(int)

    # Build the missing-value mask (1 if missing, 0 otherwise)
    missing_matrix = df[valid_missing_cols].isnull().astype(int)

    # Append the binary flag to the mask
    missing_matrix[binary_flag_name] = df[binary_flag_name]

    # Compute and return the correlation matrix
    return missing_matrix.corr()