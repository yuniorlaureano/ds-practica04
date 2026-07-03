from util.config import config
from mssql_python import connect
import pandas as pd
from typing import Iterable, List
from util.csv_reader_helper import CsvReader, ValidationRuleBase

class DataBaseOperation:

    def fetch_all_as_dataframe(self, query, params=None):
        """Get all records from database as a pandas DataFrame"""
        with connect(config.CON_STRING) as conn:
            result = pd.read_sql_query(query, conn, params)
        return result
    
    def def_fetch_all(self, query, params=None):
        """Get all records from database"""
        with connect(config.CON_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
        return result
    
    def create(self, query, params=None, return_id=False):
        """Create a new record in the databse"""
        with connect(config.CON_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if return_id:
                new_id = cursor.fetchone()[0]
                return new_id
            conn.commit()
            
    def update(self, query, params=None):
        """Update a record in the database"""
        with connect(config.CON_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def delete(self, query, params=None):
        """Delete a record from the database"""
        with connect(config.CON_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def execute(self, query, params=None):
        with connect(config.CON_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def bulk_copy(self, table_name: str, data: Iterable[tuple], columns: List[str], batch_size=10_000):
        """
        Insert data in bulk:
            data = [
                (100, "Alice"),
                (200, "Bob"),
            ]

            result = cursor.bulkcopy(
                "Users",
                data,
                keep_identity=True,
                column_mappings=["UserID", "Name"],
            )
        """
        with connect(config.CON_STRING) as conn:
            cursor = conn.cursor()
            cursor.bulkcopy(
                table_name,
                data,
                batch_size=batch_size,
                keep_identity=True,
                column_mappings=columns
            )
            conn.commit()


    def bulk_copy_csv(self, csv_path: str, table_name: str, columns: List[str], chunk_size=2000, validator: ValidationRuleBase = ValidationRuleBase()):
            print(f"**************************************************************")
            print(f"Reading data from csv '{csv_path}'")
            print(f"Starting bulkcopy process for table '{table_name}'")
            csv_reader = CsvReader()       
            def process_callback(cursor):
                def callback(rows_as_tuple):
                    print(f"Inserting {len(rows_as_tuple)} rows")
                    try:
                        cursor.bulkcopy(
                            table_name,
                            rows_as_tuple,
                            batch_size=chunk_size,
                            keep_identity=True,
                            column_mappings=columns
                        )
                    except Exception as e:
                        print("Error inserting data: ", e)
                        print(columns)
                        print(rows_as_tuple)
                        raise
                return callback


            with connect(config.CON_STRING) as conn:
                cursor = conn.cursor()
                total_inserted_rows = csv_reader.stream_csv_to_process_using_native_csv(csv_path, chunk_size, process_callback=process_callback(cursor), validator=validator)
                conn.commit()
                print(f"Insertion completed for table '{table_name}', {total_inserted_rows} inserted")
                print("-----------------------------------------------------------")

    
    