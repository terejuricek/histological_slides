import pandas as pd
import os
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

def order(output, column1, column2=None):
    """Sorts the CSV file by the specified column and saves it."""
    if os.path.exists(output):
        df = pd.read_csv(output)
        if column1 in df.columns:
            if column2:
                if column2 in df.columns:
                    df = df.sort_values(by=[column1, column2])
                    print(f"CSV file sorted by {column1} and {column2} and saved.")
                else:
                    print(f"Column '{column2}' not found in the CSV file. Sorting by {column} only.")
                    df = df.sort_values(by=column1)
            else:
                df = df.sort_values(by=column1)
                print(f"CSV file sorted by {column1} and saved.")
            df.to_csv(output, index=False)
        else:
            print(f"Column '{column1}' not found in the CSV file.")
    else:
        print("CSV file does not exist.")
        
def known_stain(stain):
    known_stains = stain_columns = ['HE', 'CD3', 'CD8', 'FoxP3', 'PD1', 'PD-L1', 'CAIX', 'CD68', 'CD45RO']
    for name in known_stains:
        if stain == name: 
            expected = True
            break
        else:
            expected = False
    return expected

# check scan_logs.txt files for compatible structure:
def stain_check(stain):
    expected = known_stain(stain)    
    double_stain = False
    
    if not expected:
        if "_" in stain:
            stain1, stain2 = stain.split("_")
            double_stain = True

    if expected:
        stain_list = [stain]
    elif double_stain:
        stain_list = [stain1, stain2]
    else:
        stain_list = [pd.NA]

    return stain_list

def add_row(df, patient_ID, slide_ID, section, slide, stain):
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
            
            if stain_check(stain) == pd.NA:
                print(f"Unrecognized staining method: {stain}")
            elif len(stain_check(stain)) == 1:
                if stain not in df.columns:
                    df[stain] = pd.NA
                    print(f"Unrecognized stainingmethod: {stain}")
                else:
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
                    # add_row(df, patient_ID, slide_ID, section, slide, stain)
            else:
                stain1, stain2 = stain_check(stain)
                if stain1 not in df.columns:
                    df[stain2] = pd.NA
                    print(f"Unrecognized staining method: {stain1}")
                else:
                    mask = (df['patient_ID'] == patient_ID) & (df['slide_ID'] == slide_ID) & (df['section'] == section) & (df['slide'] == slide)
                    if not mask.any():
                        new_entry = pd.DataFrame({
                            "patient_ID": [patient_ID],
                            "slide_ID": [slide_ID],
                            "section": [section],
                            "slide": [slide],
                            stain1: [True]
                        })
                        df = pd.concat([df, new_entry], ignore_index=True)
                    else:
                        df.loc[mask, stain1] = True  
                    # add_row(df, patient_ID, slide_ID, section, slide, stain1)
                
                if stain2 not in df.columns:
                    df[stain2] = pd.NA
                    print(f"Unrecognized staining method: {stain2}")
                else:
                    mask = (df['patient_ID'] == patient_ID) & (df['slide_ID'] == slide_ID) & (df['section'] == section) & (df['slide'] == slide)
                    if not mask.any():
                        new_entry = pd.DataFrame({
                            "patient_ID": [patient_ID],
                            "slide_ID": [slide_ID],
                            "section": [section],
                            "slide": [slide],
                            stain2: [True]
                        })
                        df = pd.concat([df, new_entry], ignore_index=True)
                    else:
                        df.loc[mask, stain2] = True  
                    # add_row(df, patient_ID, slide_ID, section, slide, stain2)
            
            
            # mask = (df['patient_ID'] == patient_ID) & (df['slide_ID'] == slide_ID) & (df['section'] == section) & (df['slide'] == slide)
            # if not mask.any():
            #     new_entry = pd.DataFrame({
            #         "patient_ID": [patient_ID],
            #         "slide_ID": [slide_ID],
            #         "section": [section],
            #         "slide": [slide],
            #         stain: [True]
            #     })
            #     df = pd.concat([df, new_entry], ignore_index=True)
            # else:
            #     df.loc[mask, stain] = True
    
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
    
    df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df1['patient_ID'] = pd.to_numeric(df1['patient_ID'])
    df1['slide'] = pd.to_numeric(df1['slide'])
    df2['patient_ID'] = pd.to_numeric(df2['patient_ID'])
    df2['slide'] = pd.to_numeric(df2['slide'])
    
    # align the DataFrames based on the first three columns
    common_columns = ["patient_ID", "slide_ID", "slide"]
    df1_aligned = df1.set_index(common_columns)
    df2_aligned = df2.set_index(common_columns)
    
    diff1 = df1_aligned[~df1_aligned.index.isin(df2_aligned.index)].copy()
    diff1 = diff1.reset_index()[common_columns]
    diff1['status'] = f"Only in {input_csv1}"
    
    diff2 = df2_aligned[~df2_aligned.index.isin(df1_aligned.index)].copy()
    diff2 = diff2.reset_index()[common_columns]
    diff2['status'] = f"Only in {input_csv2}"
    
    differences = pd.concat([diff1, diff2])
    
    result = f"Differences:\n{differences.to_string(index=False)}"
    
    if output_txt:
        with open(output_txt, 'w') as file:
            file.write(result)
        print(f"Differences saved to {output_txt}")
    else:
        print(result)


def compareCSVstains(original_csv, stored_csv, output_txt, missing=False):
    """Finds missing staining scans and saves them to a text file."""
    
    # CHANGE!!!!! = FoxP3 = FOXP3 PD-L1 = PDL1 in original_table.csv !!!!!!!!!!!!!!!!!!!
    
    df_original = pd.read_csv("original_table.csv", usecols=['patient_ID', 'slide_ID', 'slide', 'HE', 'CD3', 'CD8', 'FoxP3', 'PD1', 'PD-L1', 'CAIX', 'CD68', 'CD45RO'])
    df_stored = pd.read_csv(stored_csv)
    
    stain_columns = ['HE', 'CD3', 'CD8', 'FoxP3', 'PD1', 'PD-L1', 'CAIX', 'CD68', 'CD45RO']
    print(f"Stain columns: {stain_columns}")
    
    for stain in stain_columns:
        if stain not in df_stored.columns:
            df_stored[stain] = False

    missing_stains = []
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    # iterate through original_table
    for _, row in df_original.iterrows():
        patient_id, slide_id, slide = row['patient_ID'], row['slide_ID'].strip(), row['slide']
        
        for stain in stain_columns:
            print(f"Checking {patient_id}, {slide_id}, {slide}, {stain}")
            print(f"{row[stain]} is {pd.notna(row[stain])} and {is_number(row[stain])}")
            if pd.notna(row[stain]) and is_number(row[stain]):
                if int(row[stain]) > 0:
                    if stain == "FoxP3":
                        stain = "FOXP3"
                    elif stain == "PD-L1":
                        stain = "PDL1"
                    mask = (
                        (df_stored['patient_ID'] == patient_id) &
                        (df_stored['slide_ID'] == slide_id) &
                        (df_stored['slide'] == slide) &
                        (df_stored[stain] == True)  
                    )
                    
                    if not mask.any():  
                        missing_stains.append(f"{patient_id},{slide_id},{slide},{stain}\n")
            if missing and pd.notna(row[stain]) and row[stain] == "m":
                mask = (
                    (df_stored['patient_ID'] == patient_id) &
                    (df_stored['slide_ID'] == slide_id) &
                    (df_stored['slide'] == slide) &
                    (df_stored[stain] == True)  
                )
                
                if not mask.any():  
                    missing_stains.append(f"{patient_id},{slide_id},{slide},{stain}-missing slide\n")
    
    with open(output_txt, 'w') as file:
        file.write("Patient_ID,Slide_ID,Slide,Missing_Stain\n")
        file.writelines(missing_stains)
    
    print(f"Missing stains saved to {output_txt}")
    

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    subparsers = parser.add_subparsers(dest='command')

    parser_order = subparsers.add_parser('order', help='Sort the CSV file by the specified column')
    parser_order.add_argument('output', help='Output CSV file')
    parser_order.add_argument('column1', help='Column to sort by')
    parser_order.add_argument('column2', nargs='?', help='Second column to sort by')

    parser_files2csv = subparsers.add_parser('files2csv', help='Create/update a CSV file by adding data from the txt file')
    parser_files2csv.add_argument('input_txt', help='Input TXT file')
    parser_files2csv.add_argument('output_csv', help='Output CSV file')

    parser_csv2excel = subparsers.add_parser('csv2excel', help='Convert a CSV file to an Excel file')
    parser_csv2excel.add_argument('input_csv', help='Input CSV file')
    parser_csv2excel.add_argument('output_excel', help='Output Excel file')
    
    parser_excel2csv = subparsers.add_parser('excel2csv', help='Convert an Excel file to a CSV file')
    parser_excel2csv.add_argument('input_excel', help='Input Excel file')
    parser_excel2csv.add_argument('output_csv', help='Output CSV file')

    parser_compareCSV = subparsers.add_parser('compareCSV', help='Compare two CSV files and print/store the differences')
    parser_compareCSV.add_argument('input_csv1', help='First input CSV file')
    parser_compareCSV.add_argument('input_csv2', help='Second input CSV file')
    parser_compareCSV.add_argument('-t', '--txt', help='Output TXT file to store differences')

    parser_compareCSVstains = subparsers.add_parser('compareCSVstains', help="Compare two CSV files based on stains and store the differences")
    parser_compareCSVstains.add_argument('original_csv', help="Path to the original CSV file")
    parser_compareCSVstains.add_argument('stored_csv', help="Path to the stored scans CSV file")
    parser_compareCSVstains.add_argument('output_txt', help="Output file for missing stains")
    parser_compareCSVstains.add_argument('-m', '--missing', action='store_true', help="Check for missing slides")


    args = parser.parse_args()

    if args.command == 'order':
        order(args.output, args.column1, args.column2)
    elif args.command == 'files2csv':
        files2csv(args.input_txt, args.output_csv)
    elif args.command == 'csv2excel':
        csv2excel(args.input_csv, args.output_excel)
    elif args.command == 'excel2csv':
        excel2csv(args.input_excel, args.output_csv)
    elif args.command == 'compareCSV':
        compareCSV(args.input_csv1, args.input_csv2, args.txt)
    elif args.command == 'compareCSVstains':
        compareCSVstains(args.original_csv, args.stored_csv, args.output_txt, args.missing)
    else:
        print("Invalid command or arguments.")
