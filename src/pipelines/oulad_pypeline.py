from db.operations import DataBaseOperation
from util.custom_path import get_path_to_csv
from util.csv_reader_helper import CsvReader, ValidationRuleBase
from pipelines.validators import (
    AssessPlan,
    StudentInfoValidationRule,
    StudentRegistrationValidationRule,
    ClickStreamValidationRule,
    AssessDetailValidationRule)
from db.queries import CREATE_TABLES

def bulk_copy(csv_file, table_name, validator: ValidationRuleBase = ValidationRuleBase()):
    db_operations = DataBaseOperation()
    csv_reader = CsvReader()
    csv_path = get_path_to_csv(csv_file)
    csv_header = csv_reader.get_csv_header(csv_path)
    print(csv_header)
    db_operations.bulk_copy_csv(
        csv_path=csv_path, 
        table_name=table_name,
        columns=list(csv_header),
        validator=validator,
        chunk_size=50_000
    )

def create_tables():
    print("Creating tables.....")
    db_operations = DataBaseOperation()
    db_operations.execute(
        query=CREATE_TABLES
    )
        

def bulk_copy_cursos():
    bulk_copy(csv_file="cursos.csv", table_name="cursos")

def bulk_copy_vle_modules():
    bulk_copy(csv_file="vle_modules.csv", table_name="vle_modules")#, validator=AssessmentValidationRule())

def bulk_copy_assess_plan():
    bulk_copy(csv_file="assess_plan.csv", table_name="assess_plan", validator=AssessPlan())

def bulk_copy_student_info():
    bulk_copy(csv_file="student_info.csv", table_name="student_info", validator=StudentInfoValidationRule())

def bulk_copy_registrations():
    bulk_copy(csv_file="registrations.csv", table_name="registrations", validator=StudentRegistrationValidationRule())

def bulk_copy_vle_click_stream():
    bulk_copy(csv_file="vle_click_stream.csv", table_name="vle_click_stream", validator=ClickStreamValidationRule())

def bulk_copy_assess_detail():
    bulk_copy(csv_file="assess_detail.csv", table_name="assess_detail", validator=AssessDetailValidationRule())

def bulk_copy_runner():

    create_tables()

    bulk_copy_cursos()

    bulk_copy_vle_modules()

    bulk_copy_assess_plan()

    bulk_copy_student_info()

    bulk_copy_registrations()

    bulk_copy_vle_click_stream()

    bulk_copy_assess_detail()