import pandas as pd
import os
import sys
import argparse

def parse_filename(filename):
    """extracts patient_ID, slide_ID, section, slide, and stain method from the filename"""
    parts = filename.replace('.mrxs', '').split('-')
    patient_ID = int(parts[0][2:])
    section = parts[1]
    slide = int(parts[2])
    stain = parts[3]
    if parts[0][2] == '0':
        slide_ID = f"{parts[0][0:2]}-{parts[0][3:]}"
    else:
        slide_ID = f"{parts[0][0:2]}-{parts[0][2:]}"
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
        df = pd.DataFrame(columns=["patient_ID", "slide_ID", "section", "slide"])
    
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

def excel2csv(input_excel, output_csv):
    """Converts an Excel file to a CSV file."""
    df = pd.read_excel(input_excel)
    df.to_csv(output_csv, index=False)
    print(f"Excel file {input_excel} converted to CSV file {output_csv}")

def compareCSV(input_csv1, input_csv2, output_txt=None):
    """compares two CSV files and prints / stores (in a .txt file) the differences."""
    df1 = pd.read_csv(input_csv1)
    df2 = pd.read_csv(input_csv2)
    
    # Clean the data: strip whitespace and convert to appropriate types
    df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df1['patient_ID'] = pd.to_numeric(df1['patient_ID'])
    df1['slide'] = pd.to_numeric(df1['slide'])
    df2['patient_ID'] = pd.to_numeric(df2['patient_ID'])
    df2['slide'] = pd.to_numeric(df2['slide'])
    
    # Align the DataFrames based on the first four columns
    common_columns = ["patient_ID", "slide_ID", "slide"]
    df1_aligned = df1.set_index(common_columns)
    df2_aligned = df2.set_index(common_columns)
    
    # Find rows that are in df1 but not in df2
    diff1 = df1_aligned[~df1_aligned.index.isin(df2_aligned.index)].copy()
    diff1 = diff1.reset_index()[common_columns]
    # diff1['status'] = 'Only in first file'
    diff1['status'] = f"Only in {input_csv1}"
    
    # Find rows that are in df2 but not in df1
    diff2 = df2_aligned[~df2_aligned.index.isin(df1_aligned.index)].copy()
    diff2 = diff2.reset_index()[common_columns]
    # diff2['status'] = 'Only in second file'
    diff2['status'] = f"Only in {input_csv2}"
    
    # Combine the differences
    differences = pd.concat([diff1, diff2])
    
    result = f"Differences:\n{differences.to_string(index=False)}"
    
    if output_txt:
        with open(output_txt, 'w') as file:
            file.write(result)
        print(f"Differences saved to {output_txt}")
    else:
        print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    subparsers = parser.add_subparsers(dest='command')

    parser_order = subparsers.add_parser('order', help='Sort the CSV file by the specified column')
    parser_order.add_argument('output', help='Output CSV file')
    parser_order.add_argument('column', help='Column to sort by')

    parser_files2csv = subparsers.add_parser('files2csv', help='Create/update a CSV file by adding data from the txt file')
    parser_files2csv.add_argument('input_txt', help='Input TXT file')
    parser_files2csv.add_argument('output_csv', help='Output CSV file')

    parser_csv2excel = subparsers.add_parser('csv2excel', help='Convert a CSV file to an Excel file')
    parser_csv2excel.add_argument('input_csv', help='Input CSV file')
    parser_csv2excel.add_argument('output_excel', help='Output Excel file')
    
    parser_excel2csv = subparsers.add_parser('excel2csv', help='Convert a Excel file to an CSV file')
    parser_excel2csv.add_argument('input_excel', help='Input Excel file')
    parser_excel2csv.add_argument('output_csv', help='Output CSV file')

    parser_compareCSV = subparsers.add_parser('compareCSV', help='Compare two CSV files and print/store the differences')
    parser_compareCSV.add_argument('input_csv1', help='First input CSV file')
    parser_compareCSV.add_argument('input_csv2', help='Second input CSV file')
    parser_compareCSV.add_argument('-t', '--txt', help='Output TXT file to store differences')

    args = parser.parse_args()

    if args.command == 'order':
        order(args.output, args.column)
    elif args.command == 'files2csv':
        files2csv(args.input_txt, args.output_csv)
    elif args.command == 'csv2excel':
        csv2excel(args.input_csv, args.output_excel)
    elif args.command == 'excel2csv':
        excel2csv(args.input_excel, args.output_csv)
    elif args.command == 'compareCSV':
        compareCSV(args.input_csv1, args.input_csv2, args.txt)
    else:
        print("Invalid command or arguments.")
