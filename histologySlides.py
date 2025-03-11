import pandas as pd
import os
import argparse


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
                    print(f"Column {column2} not found in the CSV file. Sorting by {column1} only.")
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
    known_stains = ['HE', 'CD3', 'CD8', 'FoxP3', 'PD1', 'PD-L1', 'CAIX', 'CD68', 'CD45RO']
    for name in known_stains:
        if stain == name:
            return True
    return False

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
                    print(f"Column {column2} not found in the CSV file. Sorting by {column1} only.")
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
    known_stains = ['HE', 'CD3', 'CD8', 'FoxP3', 'PD1', 'PD-L1', 'CAIX', 'CD68', 'CD45RO']
    for name in known_stains:
        if stain == name:
            return True
    return False

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

def compareTables(input_csv1, input_csv2, output_txt=None):
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


def compareStains(original_csv, stored_csv, output_txt=None, missing=False, verbose=False):
    """Finds missing staining scans and saves them to a text file."""
    
    # CHANGE!!!!! = FoxP3 = FOXP3 PD-L1 = PDL1 in original_table.csv !!!!!!!!!!!!!!!!!!!
    
    # if i input the original table as an excel file
    
    if original_csv.endswith('.xlsx'):
        df_original = pd.read_excel(original_csv)
    elif original_csv.endswith('.csv'):
        df_original = pd.read_csv(original_csv)
        
    # CHANGE!!!!! = FoxP3 = FOXP3 PD-L1 = PDL1 in original_table.csv !!!!!!!!!!!!!!!!!!!
    
    # if i input the original table as an excel file
    
    if original_csv.endswith('.xlsx'):
        df_original = pd.read_excel(original_csv)
    elif original_csv.endswith('.csv'):
        df_original = pd.read_csv(original_csv)
        
    df_stored = pd.read_csv(stored_csv)
    df_original.columns = df_original.columns.str.strip().str.upper()
    df_stored.columns = df_stored.columns.str.strip().str.upper()
    
    df_original.rename(columns={"PD-L1": "PDL1"}, inplace=True)
    df_original.rename(columns={"PATIENT ID": "PATIENT_ID"}, inplace=True)
    df_original.rename(columns={"SLIDES ID": "SLIDE_ID"}, inplace=True)
    df_original.rename(columns={"SLIDES": "SLIDE"}, inplace=True)
    
    stain_columns = ['HE', 'CD3', 'CD8', 'FOXP3', 'PD1', 'PDL1', 'CAIX', 'CD68', 'CD45RO']
    print(f"Stain