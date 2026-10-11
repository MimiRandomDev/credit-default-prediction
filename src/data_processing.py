#data_processing.py
from typing import Any
import pandas as pd

def execute_query(cursor: Any, query: str) -> list[Any]:
    """
    Executes a SQL query against a database using the provided cursor and fetches all result rows.

    Parameters
    ----------
    cursor : Any
        A DB-API 2.0 compliant database cursor object (e.g., sqlite3.Cursor, psycopg2.cursor).
    query : str
        The SQL query string to be executed.

    Returns
    -------
    list[Any]
        A list containing all fetched records from the executed query.

    Examples
    --------
    >>> import sqlite3
    >>> conn = sqlite3.connect(":memory:")
    >>> cursor = conn.cursor()
    >>> cursor.execute("CREATE TABLE test (id INT);")
    >>> cursor.execute("INSERT INTO test VALUES (1);")
    >>> results = execute_query(cursor, "SELECT * FROM test;")
    >>> print(results)
    [(1,)]
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def statistical_summary(df: pd.DataFrame, column_name: str) -> dict[str, Any]:
    """
    Generates a complete statistical, data quality, and cardinality summary for a DataFrame column.

    Combines missing value analysis, unique value exploration, central tendency,
    dispersion metrics, and interquartile range (IQR) based outlier detection.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the column to analyze.
    column_name : str
        Name of the column to evaluate.

    Returns
    -------
    dict[str, Any]
        A dictionary mapping statistical and quality metric names to their calculated values:
        - 'column_name': Target column name.
        - 'data_type': Column data type.
        - 'total_count': Total number of rows.
        - 'non_null_count': Count of valid non-missing values.
        - 'null_count': Count of missing (NaN/null) values.
        - 'null_percentage': Percentage of missing values relative to total rows.
        - 'unique_count': Total count of unique elements (nunique).
        - 'unique_values': Array of unique values found.
        - 'value_counts': Pandas Series with value frequency distribution.
        - 'mean': Arithmetic average.
        - 'std': Standard deviation.
        - 'min': Minimum value.
        - 'q1': First quartile (25th percentile).
        - 'median': Median (50th percentile).
        - 'q3': Third quartile (75th percentile).
        - 'max': Maximum value.
        - 'iqr': Interquartile range (Q3 - Q1).
        - 'lower_bound': Lower threshold for outlier detection (Q1 - 1.5 * IQR).
        - 'upper_bound': Upper threshold for outlier detection (Q3 + 1.5 * IQR).
        - 'outliers_count': Total number of identified outliers.
        - 'outliers': Pandas Series containing the detected outlier values.

    Examples
    --------
    >>> summary = statistical_summary(df, "educacion")
    >>> print(summary["unique_count"])
    >>> print(summary["null_percentage"])
    """
    series = df[column_name]

    # 1. Quality & Missing Data
    total_count = len(series)
    null_count = int(series.isna().sum())
    non_null_count = total_count - null_count
    null_percentage = round((null_count / total_count * 100), 2) if total_count > 0 else 0.0

    # 2. Cardinality & Unique Values
    unique_count = int(series.nunique())
    unique_vals = series.unique()
    val_counts = series.value_counts()

    # 3. Descriptive Statistics
    is_numeric = pd.api.types.is_numeric_dtype(series)

    mean = float(series.mean()) if is_numeric else None
    std = float(series.std()) if is_numeric else None
    min_val = series.min() if is_numeric else None
    q1 = float(series.quantile(0.25)) if is_numeric else None
    median = float(series.median()) if is_numeric else None
    q3 = float(series.quantile(0.75)) if is_numeric else None
    max_val = series.max() if is_numeric else None

    # 4. Outlier Analysis (IQR Method)
    if is_numeric and q1 is not None and q3 is not None:
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers_series = series[(series < lower_bound) | (series > upper_bound)]
        outliers_count = len(outliers_series)
    else:
        iqr = lower_bound = upper_bound = None
        outliers_series = pd.Series(dtype=object)
        outliers_count = 0

    return {
        "column_name": column_name,
        "data_type": str(series.dtype),
        "total_count": total_count,
        "non_null_count": non_null_count,
        "null_count": null_count,
        "null_percentage": null_percentage,
        "unique_count": unique_count,
        "unique_values": unique_vals,
        "value_counts": val_counts,
        "mean": mean,
        "std": std,
        "min": min_val,
        "q1": q1,
        "median": median,
        "q3": q3,
        "max": max_val,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outliers_count": outliers_count,
        "outliers": outliers_series
    }



if __name__ == "__main__":
    pass
