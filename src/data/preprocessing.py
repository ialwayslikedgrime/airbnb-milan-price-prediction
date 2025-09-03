import pandas as pd
from typing import List

def impute_and_create_binary_feature(df, column_name, default_value="No description provided"):
    """
    Impute missing values in a specified column with a default value and create a binary indicator.

    Parameters:
    df (pd.DataFrame): The dataframe to process.
    column_name (str): The column to impute and create a binary feature for.
    default_value (str): The default value to impute missing values with.

    Returns:
    pd.DataFrame: The updated dataframe with the new binary feature and without the original column.
    """
    df[column_name] = df[column_name].fillna(default_value)
    binary_column_name = f"{column_name}_present"
    df[binary_column_name] = (df[column_name] != default_value).astype(int)
    
    # Drop the original column
    df = df.drop(columns=[column_name])
    
    # Print percentage distribution
    percentage = df[binary_column_name].value_counts(normalize=True) * 100
    print(percentage)

    return df



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple

def plot_missing_corr_heatmap(
    df: pd.DataFrame,
    missing_columns: List[str],
    indicator_col: str = "number_of_reviews",
    figsize: Tuple[int, int] = (12, 8),
    cmap: str = "coolwarm",
    annot: bool = True,
    fmt: str = ".2f",
    linewidths: float = 0.5,
    title: str = "Correlation of Missing-Value Indicators",
) -> pd.DataFrame:
    """
    Compute the correlation matrix between:
      • a binary mask of missing values for the specified columns, and
      • a binary flag that is 1 when `indicator_col` equals 0 and 0 otherwise;
    then plot the resulting heatmap.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to analyse.
    missing_columns : list[str]
        Columns for which to create missing-value indicators.
    indicator_col : str, default "number_of_reviews"
        Numeric column used to create the 0-vs-other flag.
    figsize : tuple[int, int], default (12, 8)
        Figure size for the heatmap.
    cmap : str, default "coolwarm"
        Colour map for the heatmap.
    annot : bool, default True
        Whether to annotate cells with correlation values.
    fmt : str, default ".2f"
        Format string for annotations.
    linewidths : float, default 0.5
        Grid line width between cells.
    title : str, default "Correlation of Missing-Value Indicators"
        Title shown above the heatmap.

    Returns
    -------
    pd.DataFrame
        The correlation matrix that was plotted.

    Raises
    ------
    ValueError
        If none of the requested `missing_columns` are present in `df`.
    """
    # 1. Keep only columns present in the DataFrame
    valid_missing_cols = [c for c in missing_columns if c in df.columns]
    if not valid_missing_cols:
        raise ValueError("None of the specified columns are present in the DataFrame.")

    # 2. Create the 0-vs-other binary flag
    binary_flag_name = f"{indicator_col}_0_vs_other"
    df = df.copy()                                   # avoid mutating the original DataFrame
    df[binary_flag_name] = (df[indicator_col] == 0).astype(int)

    # 3. Build the missing-value mask (1 if missing, 0 otherwise)
    missing_matrix = df[valid_missing_cols].isnull().astype(int)

    # 4. Append the binary flag to the mask
    missing_matrix[binary_flag_name] = df[binary_flag_name]

    # 5. Compute the correlation matrix
    corr = missing_matrix.corr()

    # 6. Plot the heatmap
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot, cmap=cmap, fmt=fmt, linewidths=linewidths)
    plt.title(title)
    plt.show()

    return corr



def partially_missing(df, review_columns):

    # Conta quanti valori mancanti ci sono per riga nelle colonne delle review
    df["num_missing_reviews"] = df[review_columns].isnull().sum(axis=1)

    # Filtra solo le righe che hanno almeno un valore mancante nei review scores
    df_missing_reviews = df[df["num_missing_reviews"] > 0]

    print(f"Listings con almeno un valore di review mancante: {len(df_missing_reviews)}")

    # Identifica le righe che hanno TUTTE le review scores mancanti
    all_missing = df_missing_reviews[review_columns].isnull().all(axis=1).sum()

    print(f"Listings dove TUTTE le review scores sono mancanti: {all_missing}")

    # Identifica i listing con alcune ma non tutte le review scores mancanti
    df_partial_missing_reviews = df_missing_reviews[~df_missing_reviews[review_columns].isnull().all(axis=1)]

    # Include host_url for manual verification
    columns_to_display = review_columns + ["id"] + ["listing_url"] + ["number_of_reviews"]
    
    # Display results (only review score columns + host URL)
    print(f"Listings with some but not all review scores missing: {len(df_partial_missing_reviews)}")

    ids_partial_missing = df_partial_missing_reviews["id"].tolist()

    return df_partial_missing_reviews[columns_to_display], [ids_partial_missing]



import pandas as pd
from typing import Sequence, Tuple, List, Any


def partial_review_missing(
    df: pd.DataFrame,
    review_cols: Sequence[str],
    *,
    id_col: str = "id",
    extra_cols: Sequence[str] | None = ("listing_url", "number_of_reviews"),
) -> Tuple[pd.DataFrame, List[Any]]:
    """
    Print a summary—and return the offending rows—where some but not all
    review-score fields are missing.  **Does not add any columns** to *df*.

    Parameters
    ----------
    df : pd.DataFrame
        Source data.
    review_cols : Sequence[str]
        Columns containing review scores.
    id_col : str, default "id"
        Primary key column.
    extra_cols : Sequence[str] | None, optional
        Additional columns to keep in the returned DataFrame.

    Returns
    -------
    partial_df : pd.DataFrame
        Rows with partial missing review scores.
    ids : list
        Values from *id_col* for those rows.
    """
    # Boolean masks
    any_missing = df[review_cols].isnull().any(axis=1)
    all_missing = df[review_cols].isnull().all(axis=1)
    partial_mask = any_missing & ~all_missing

    # Counts for console output
    n_any_missing = int(any_missing.sum())
    n_all_missing = int(all_missing.sum())
    n_partial = int(partial_mask.sum())

    print(f"Listings with at least one missing review score: {n_any_missing}")
    print(f"Listings where all review scores are missing: {n_all_missing}")
    print(f"Listings with some but not all review scores missing: {n_partial}")

    # Build the return DataFrame (no mutation of the original df)
    cols_to_return: List[str] = [id_col]
    if extra_cols:
        cols_to_return.extend(extra_cols)
    cols_to_return.extend(review_cols)

    partial_df = df.loc[partial_mask, cols_to_return].copy()
    ids = partial_df[id_col].tolist()

    return partial_df, ids