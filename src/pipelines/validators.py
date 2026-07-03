from util.csv_reader_helper import ValidationRuleBase
from typing import List
from datetime import datetime

class AssessmentValidationRule(ValidationRuleBase):
    def transform(self, row: List[str]) -> List:
        return [
            row[0],
            row[1],
            row[2],
            row[3],
            row[4] if row[4].strip() != '' else None,
            row[5]
        ]

class VleValidationRule(ValidationRuleBase):
    def transform(self, row: List[str]) -> List:
        return [
            row[0],
            row[1],
            row[2],
            row[3],
            row[4] if row[4].strip() != '' else None,
            row[5] if row[5].strip() != '' else None,
        ]
    
class AssessPlan(ValidationRuleBase):
    def __init__(self):
        super().__init__()
        self.inserted = {}
    
    def validate(self, row):
        if row[2] in self.inserted:
            return False
        
        self.inserted[row[2]] = True
        return True
    
class StudentInfoValidationRule(ValidationRuleBase):
     def transform(self, row: List[str]) -> List:
        return [
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8] if row[8].strip() != '' else None,
            row[9] if row[9].strip() != '' else None,
            row[10],
            row[11]
        ]

class StudentRegistrationValidationRule(ValidationRuleBase):
    def transform(self, row: List[str]) -> List:
        return [
            row[0],
            row[1],
            row[2],
            row[3] if row[3].strip() != '' else None,
            row[4] if row[4].strip() != '' else None,
        ]
    
class ClickStreamValidationRule(ValidationRuleBase):
    
    def format_date(self, date_str):
        if date_str.strip() == '':
            return None
        else:
            date_parts = date_str.split(".")
            if len(date_parts) == 3:
                day, month, year = date_parts
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            else:
                return None
    def transform(self, row: List[str]) -> List:
        return [
            row[0],
            row[1],
            row[2] if row[2].strip() != '' else None,
            row[3] if row[3].strip() != '' else None,
            row[4],
            self.format_date(row[5]),
            self.format_date(row[6]),
            row[7],
            row[8],
            row[9] if row[9].strip() != '' else None,
            row[10] if row[10].strip() != '' else None,
            row[11] if row[11].strip() != '' else None,
            row[12]
        ]
    
class AssessDetailValidationRule(ValidationRuleBase):
    def format_date(self, date_str):
        if date_str.strip() == '':
            return None
        else:
            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%y %I:%M %p")
                return date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None
            
    def transform(self, row: List[str]) -> List:
        return [
            row[0], # guid_student_id         UNIQUEIDENTIFIER NOT NULL,
            row[1], # guid_assess_id          UNIQUEIDENTIFIER NOT NULL,
            self.format_date(row[2]), # date_submitted          DATETIME         NULL,
            row[3], # is_banked               BIT              NOT NULL DEFAULT (0),
            row[4], # score                   DECIMAL(6,2)     NULL,
            row[5], # assessment_type         VARCHAR(10)      NULL,
            self.format_date(row[6]), # [date]                  DATETIME         NULL,
            row[7], # weight                  TINYINT          NULL,
            row[8], # gender                  VARCHAR(30)      NULL,
            row[9], # region                  VARCHAR(30)      NULL,
            row[10], # highest_education       VARCHAR(40)      NULL,
            row[11], # imd_band                VARCHAR(10)      NULL,
            row[12], # age_band                VARCHAR(10)      NULL,
            row[13], # num_of_prev_attempts    TINYINT          NULL,
            row[14], # studied_credits         SMALLINT         NULL,
            row[15], # disability              CHAR(1)          NULL,
            row[16], # final_result            VARCHAR(20)      NULL,
            row[17], # status                  VARCHAR(20)      NULL,
            row[18], # module                  VARCHAR(10)      NULL,
            row[19], # presentation            VARCHAR(10)      NULL,
            row[20], # date_real_days          SMALLINT         NULL,
            row[21], # id_assetcode            INT              NULL,
        ]