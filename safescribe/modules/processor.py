from pathlib import Path
from pypdftk import compress, uncompress
import re
import json

def compress_pdf(input_file, output_file):
    try:
        compress(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Error compressing PDF: {str(e)}")

def uncompress_pdf(input_file, output_file):
    try:
        uncompress(input_file, output_file)
    except Exception as e:
        raise RuntimeError(f"Error decompressing PDF: {str(e)}")

def cleanup_temp_files(*file_paths):
    for file_path in file_paths:
        path = Path(file_path)
        if path.exists():
            path.unlink()

def remove_links(input_file, output_file):

    page_count = 0
    url_count = 0
    link_count = 0
    removed_links = []

    with open(input_file, 'rb') as file_to_be_sanitized, open(output_file, "wb") as newPdf:
        for line in file_to_be_sanitized:
            output = line.decode('latin-1')

            if("/Type /Page\n" in output):
                page_count += 1
                no_change = output.encode("latin-1")
                newPdf.write(no_change)

            elif ("/URI (" in output):
                parentheses = output[output.find("(")+1:output.find(")")]
                regex = r"^(.*?)(?: \((.*)\))?$"
                no_parentheses = re.sub("([\(\[]).*?([\)\]])","()", output)
                
                removed_links.append({
                    "page": page_count,
                    "type": "/URI",
                    "data": parentheses,
                    "line": output.strip()
                })

                change_into = no_parentheses.encode("latin-1")
                newPdf.write(change_into)
                url_count = url_count + 1

            elif("/Subtype /Link" in output):
                replace_type = output.replace("/Link", "/Type0")

                removed_links.append({
                    "page": page_count,
                    "type": "/Subtype",
                    "data": "/Link",
                    "line": output.strip()
                })

                change_into = replace_type.encode("latin-1")
                newPdf.write(change_into)
                link_count = link_count + 1
            
            else:
                no_change = output.encode("latin-1")
                newPdf.write(no_change)
    
    return page_count, url_count, link_count, removed_links

def remove_actions(input_file, output_file):
    
    page_count = 0
    action_count = 0
    removed_actions = []

    with open(input_file, 'rb') as file_to_be_sanitized, open(output_file, "wb") as newPdf:
        for line in file_to_be_sanitized:
            output = line.decode('latin-1')

            if("/Type /Page\n" in output):
                page_count += 1
                no_change = output.encode("latin-1")
                newPdf.write(no_change)

            elif ("/Type /Action" in output):
                replace_type = output.replace("/Action", "/Type0")

                removed_actions.append({
                    "page": page_count,
                    "type": "/A",
                    "data": "/Action",
                    "line": output.strip()
                })

                action_count += 1

                change_into = replace_type.encode("latin-1")
                newPdf.write(change_into)
            
            else:
                no_change = output.encode("latin-1")
                newPdf.write(no_change)

    return page_count, action_count, removed_actions

def remove_specific_actions(input_file, output_file, actions_to_remove):
    page_count = 0
    action_count = 0
    removed_actions = []

    action_mappings = {
        "GoTo": "/GoTo",
        "GoToR": "/GoToR",
        "GoToE": "/GoToE",
        "Launch": "/Launch",
        "Thread": "/Thread",
        "URI": "/URI",
        "Sound": "/Sound",
        "Movie": "/Movie",
        "Hide": "/Hide",
        "Named": "/Named",
        "SubmitForm": "/SubmitForm",
        "ResetForm": "/ResetForm",
        "ImportData": "/ImportData",
        "JavaScript": "/JavaScript",
        "SetOCGState": "/SetOCGState",
        "Rendition": "/Rendition",
        "Trans": "/Trans",
        "GoTo3DView": "/GoTo3DView"
    }

    with open(input_file, 'rb') as file_to_be_sanitized, open(output_file, "wb") as newPdf:
        for line in file_to_be_sanitized:
            output = line.decode('latin-1')

            if "/Type /Page\n" in output:
                page_count += 1
                no_change = output.encode("latin-1")
                newPdf.write(no_change)
            
            elif "/S /" in output:

                for action, pattern in action_mappings.items():
                    if action in actions_to_remove and pattern in output:
                        replace_type = output.replace(pattern, "/None")
                        removed_actions.append({
                            "page": page_count,
                            "type": "/S",
                            "data": pattern,
                            "line": output.strip()
                        })
                        action_count += 1
                        change_into = replace_type.encode("latin-1")
                        newPdf.write(change_into)
                        break

            else:
                no_change = output.encode("latin-1")
                newPdf.write(no_change)

    return page_count, action_count, removed_actions