import json
import csv

def jsonl_to_csv(jsonl_file, csv_file):
    """
    Converts a JSONL file to a CSV file.
    
    :param jsonl_file: Path to the input JSONL file.
    :param csv_file: Path to the output CSV file.
    """
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as infile, open(csv_file, 'w', encoding='utf-8', newline='') as outfile:
            first_line = infile.readline()
            if not first_line:
                print("The JSONL file is empty.")
                return
            first_obj = json.loads(first_line)
            headers = list(first_obj.keys())
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow(first_obj)

            for line in infile:
                obj = json.loads(line)
                writer.writerow(obj)
                
        print(f"Successfully converted {jsonl_file} to {csv_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

input_file_location = input("Enter the location of the JSONL file: ")
output_file_location = input("Enter the location of the CSV file: ")
jsonl_to_csv(input_file_location, output_file_location)
