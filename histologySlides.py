import pandas as pd
import os
import sys

def parse_filename(filename):
    """extracts patient_ID, slide_ID, section, slide, and stain method from the filename"""
    parts = filename.replace('.mrxs', '').split('-')
    patient_ID = parts[0][2:]  
    section = parts[1]
    slide = parts[2]
    stain = parts[3]
    slide_ID = parts[0]
    return patient_ID, slide_ID, section, slide, stain

def order(output, column):
    """Sorts the CSV file by the specified column and saves it."""
    if os.path.exists(output):
        df = pd.read_csv(output)
        if column in df.columns:
            df = df.sort_values(by=column)
            df.to_csv(output, index=False)
            print(f"CSV file sorted by {column} and saved.")
        else:
            print(f"Column '{column}' not found in the CSV file.")
    else:
        print("CSV file does not exist.")

def files2csv(input_txt, output_csv):
    """creates / updates a CSV file by adding data from the txt file."""
    if os.path.exists(output_csv):
        df = pd.read_csv(output_csv)
    else:
        df = pd.DataFrame(columns=["patient_ID", "slide_ID", "section", "slide"])  # Initial columns
    
    new_entries = []
    stains = set(df.columns[4:])
    
    with open(input_txt, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                patient_ID, slide_ID, section, slide, stain = parse_filename(line)

            if stain not in df.columns:
                df[stain] = pd.NA
            
            mask = (df['patient_ID'] == patient_ID) & (df['slide_ID'] == slide_ID) & (df['section'] == section) & (df['slide'] == slide)
            if not mask.any():
                new_entry = pd.DataFrame({
                    "patient_ID": [patient_ID],
                    "slide_ID": [slide_ID],
                    "section": [section],
                    "slide": [slide],
                    stain: [True]
                })
                df = pd.concat([df, new_entry], ignore_index=True)
            else:
                df.loc[mask, stain] = True
    
    df.to_csv(output_csv, index=False)
    print(f"updated CSV saved to {output_csv}")

def csv2excel(input_csv, output_excel):
    """Converts a CSV file to an Excel file."""
    df = pd.read_csv(input_csv)
    df.to_excel(output_excel, index=False)
    print(f"CSV file {input_csv} converted to Excel file {output_excel}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <command> <args>...")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "order" and len(sys.argv) == 4:
        order(sys.argv[2], sys.argv[3])
    elif command == "files2csv" and len(sys.argv) == 4:
        files2csv(sys.argv[2], sys.argv[3])
    elif command == "csv2excel" and len(sys.argv) == 4:
        csv2excel(sys.argv[2], sys.argv[3])
    else:
        print("Invalid command or arguments.")
