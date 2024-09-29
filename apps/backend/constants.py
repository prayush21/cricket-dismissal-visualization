import os

# Get the absolute path of the current file (constants.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one directory to reach the 'backend' folder
backend_dir = os.path.dirname(current_dir)

cricket_format_dict = {
    "ODI": {"file_name": os.path.join(backend_dir, "backend/odis_json")},
    "IPL": {"file_name": os.path.join(backend_dir, "backend/ipl_json")},
    "T20": {"file_name": os.path.join(backend_dir, "backend/t20s_json")},    
}

__all__ = ['cricket_format_dict']