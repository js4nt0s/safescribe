import json
from datetime import datetime

def start_log_session(log_file_path):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'--- Log Session Started at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---\n')

def log_summary(log_file_path, input_file_name, page_count, url_count, link_count, action_count=None):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = (
        f"Date and Time: {current_time}\n"
        f"Input File: {input_file_name}\n"
        f"Page Count: {page_count}\n"
        f"URL Count: {url_count}\n"
        f"Link Subtype Count: {link_count}\n"
    )
    if action_count is not None:
        summary += f"Action Count: {action_count}\n"
    
    summary += "\n"
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(summary)

def log_action(log_file_path, log_data):
    with open(log_file_path, 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_entry = json.dumps({"timestamp": timestamp, "data": log_data}, indent=4)
        log_file.write(formatted_entry + '\n')

def end_log_session(log_file_path):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'--- Log Session Ended at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---\n')

def log_divide(log_file_path):
    with open(log_file_path, 'a') as log_file:
        log_file.write("---------------------------------------------------------------------------------------------------------------\n")