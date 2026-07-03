import os

def get_path_to_csv(csv_file: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "..","..", "data", csv_file)