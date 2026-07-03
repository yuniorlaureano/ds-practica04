import csv
from itertools import islice
from typing import List
import pandas as pd
from pandas import DataFrame
from util.helper import convert_pd_to_tuple_with_sql_friendly

class CsvReaderResult:
    def __init__(self, header: tuple, rows: List[tuple]):
        self.header = header
        self.rows: List[tuple] = rows

class ValidationRuleBase:
    def transform(self, row: List[str]) -> List:
        return row
    
    def validate(self, row: List[str]) -> bool:
        return True

class CsvReader:
    
    def read_csv_using_native_csv(self, csv_path) -> List[tuple]:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            header = tuple(next(reader))
            rows = [tuple(row) for row in reader]
            result = CsvReaderResult(header, rows)
            return result
        
    def read_csv_using_pd(self, csv_path) -> DataFrame:
        df = pd.read_csv(csv_path)
        return df
    
    def stream_csv_to_process_using_pd(self, csv_path, chunk_size=2000, process_callback=None):
        chunks = pd.read_csv(csv_path, chunksize=chunk_size)
        for i, chunk in enumerate(chunks, 1):
            if process_callback:
               process_callback(convert_pd_to_tuple_with_sql_friendly(chunk))

    def stream_csv_to_process_using_native_csv(self, csv_path, chunk_size=2000, process_callback=None, validator: ValidationRuleBase = ValidationRuleBase()):
        with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            header = tuple(next(reader))
            total_read = 0
            while True:
                chunk = list(islice(reader, chunk_size))
                if not chunk:
                    break

                rows_as_tuple = [tuple(validator.transform(row)) for row in chunk if validator.validate(row)]
                total_read += len(rows_as_tuple)
                can_break = process_callback(rows_as_tuple)
                if can_break:
                     break
                
            return total_read
                
    def get_csv_header(self, csv_path):
        with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            header = tuple(next(reader))
            return header