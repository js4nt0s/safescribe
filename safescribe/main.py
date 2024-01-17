from pathlib import Path
import argparse
from rich import print
from datetime import datetime
import traceback

from modules import processor, logger

def parse_arguments():

    parser = argparse.ArgumentParser(description="SafeScribe PDF Processor")
    parser.add_argument("path", help="Path to the input PDF file")
    parser.add_argument("-o", "--output-dir", default="./output", help="Directory for output files")
    parser.add_argument("-l", "--log", action="store_true", help="Enable logging")
    
    action_types = ["GoTo", "GoToR", "GoToE", "Launch", "Thread", "URI", "Sound", 
                    "Movie", "Hide", "Named", "SubmitForm", "ResetForm", "ImportData", 
                    "JavaScript", "SetOCGState", "Rendition", "Trans", "GoTo3DView"]
    
    action_group = parser.add_mutually_exclusive_group()

    action_group.add_argument("-A", "--all-actions", action="store_true", 
                              help="Remove all action types from the PDF")
    action_group.add_argument("-a", "--actions", nargs="+", metavar="ACTION", choices=action_types,
                              help="Specify individual action types to remove. "
                                   "Available actions: " + ", ".join(action_types))

    args = parser.parse_args()

    return args

def debug(args):

    print("[orange1]-----------------------[/orange1]")
    print("[bold dark_orange]Debug Mode Activated[/bold dark_orange]")
    print("[orange1]-----------------------[/orange1]")
    print(f"Input PDF File: {args.path}")

    output_dir = args.output_dir if args.output_dir else "./output"
    print(f"Output Directory: {Path(output_dir).resolve()}")

    if args.log:
        print("Logging: Enabled")
    else:
        print("Logging: Disabled")

    if args.all_actions:
        print("Action Removal: All actions will be removed.")
    elif args.actions:
        print(f"Action Removal: Specific actions to be removed - {', '.join(args.actions)}")
    else:
        print("Action Removal: No actions will be removed.")
    
    print("[orange1]-----------------------[/orange1]")

def main():
    try:
        print("[green]Starting[/green][bold blue] Safescribe | 安全な筆記者[/bold blue]")
        
        args = parse_arguments()

        debug(args)

        input_file = Path(args.path)
        input_file_name = input_file.stem

        output_dir = args.output_dir or "./output"    
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        temp_dir = "./temp"
        temp_dir_path = Path(temp_dir)
        temp_dir_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file_name = f"{timestamp}-{input_file_name}.log"
        log_file_path = output_dir_path / log_file_name

        # Define file paths
        uncompress_pdf_output = temp_dir_path / f"temp-uncompressed-{input_file_name}.pdf"
        link_processed_output = temp_dir_path / f"temp-link-processed-{input_file_name}.pdf"
        action_processed_output = temp_dir_path / f"temp-action-processed-{input_file_name}.pdf"
        final_output = output_dir_path / f"processed-{input_file.name}"

        try:
            # Step 1: Uncompress
            processor.uncompress_pdf(input_file, uncompress_pdf_output)

            # Step 2: Process file (Link and Actions)
            page_count, url_count, link_count, removed_links = processor.remove_links(
                uncompress_pdf_output, link_processed_output)

            processor.cleanup_temp_files(uncompress_pdf_output)

            processed_file_for_compression = link_processed_output

            if args.all_actions:
                page_count, action_count, removed_actions = processor.remove_actions(
                    link_processed_output, action_processed_output)
                
                processor.cleanup_temp_files(link_processed_output)

                processed_file_for_compression = action_processed_output

            if args.actions:
                page_count, action_count, removed_actions = processor.remove_specific_actions(
                    link_processed_output, action_processed_output, args.actions)
                
                # Delete the link-processed file after actions are processed
                processor.cleanup_temp_files(link_processed_output)

                processed_file_for_compression = action_processed_output

            # Step 3: Compress file
            processor.compress_pdf(processed_file_for_compression, final_output)
            
            processor.cleanup_temp_files(processed_file_for_compression)

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            return


    except Exception as main_exception:
        print(f"A critical error occurred in the main process: {main_exception}")
        traceback.print_exc()
    
    finally:
        # Step 3.5: Cleanup temporary files
        processor.cleanup_temp_files('temp/*')

    # Step 4: Log Findings
    
    if(args.log):
        logger.start_log_session(log_file_path)

        logger.log_summary(log_file_path, input_file_name, page_count, url_count, link_count, action_count)

        for entry in removed_links:
            logger.log_action(log_file_path, entry)
        
        logger.log_divide(log_file_path)

        for entry in removed_actions:
            logger.log_action(log_file_path, entry)
        
        logger.end_log_session(log_file_path)

if __name__ == "__main__":
    main()