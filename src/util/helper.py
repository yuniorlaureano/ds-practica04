from pandas import DataFrame
import pandas as pd

def convert_pd_to_tuple(df: DataFrame):
    return [type(df) for x in df.to_numpy()]

def convert_pd_to_tuple_with_sql_friendly(df: DataFrame):
    rows = list(df.where(pd.notnull(df), None).itertuples(index=False, name=None))
    return rows