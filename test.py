import pandas as pd

def compareTables(input_csv1, input_csv2, output_csv1=None, output_csv2=None):
    """Compares two CSV files and outputs full rows that are missing in each.
    
    Args:
        input_csv1 (str): Path to the first input CSV.
        input_csv2 (str): Path to the second input CSV.
        output_csv1 (str, optional): File path to save rows from CSV1 missing in CSV2.
        output_csv2 (str, optional): File path to save rows from CSV2 missing in CSV1.
    """
    # Load data
    df1 = pd.read_csv(input_csv1)
    df2 = pd.read_csv(input_csv2)

    # Strip whitespace from strings
    df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Ensure patient_ID and slide are numeric for matching
    df1['patient_ID'] = pd.to_numeric(df1['patient_ID'])
    df1['slide'] = pd.to_numeric(df1['slide'])
    df2['patient_ID'] = pd.to_numeric(df2['patient_ID'])
    df2['slide'] = pd.to_numeric(df2['slide'])

    # Define key columns for comparison
    key_columns = ["patient_ID", "slide_ID", "slide"]

    # Align based on key columns
    df1_indexed = df1.set_index(key_columns)
    df2_indexed = df2.set_index(key_columns)

    # Rows in df1 not in df2
    missing_from_df2 = df1_indexed[~df1_indexed.index.isin(df2_indexed.index)].reset_index()

    # Rows in df2 not in df1
    missing_from_df1 = df2_indexed[~df2_indexed.index.isin(df1_indexed.index)].reset_index()

    # Output results
    if output_csv1:
        missing_from_df2.to_csv(output_csv1, index=False)
        print(f"Rows from {input_csv1} missing in {input_csv2} saved to: {output_csv1}")
    else:
        print(f"\nRows in {input_csv1} missing in {input_csv2}:\n")
        print(missing_from_df2.to_string(index=False))

    if output_csv2:
        missing_from_df1.to_csv(output_csv2, index=False)
        print(f"Rows from {input_csv2} missing in {input_csv1} saved to: {output_csv2}")
    else:
        print(f"\nRows in {input_csv2} missing in {input_csv1}:\n")
        print(missing_from_df1.to_string(index=False))
        
# compareTables("/Users/terezajurickova/Desktop/bioimaging/original_table.csv", "/Users/terezajurickova/Desktop/bioimaging/scans.csv", "/Users/terezajurickova/Desktop/bioimaging/missing_from_table2.csv", "/Users/terezajurickova/Desktop/bioimaging/missing_from_table1.csv")


# save as a new table
def addMissingLog(table, missing_list, output_csv="/Users/terezajurickova/Desktop/bioimaging/added_Missing_logs.csv"):
    """Adds a log of missing rows to a table.
    
    Args:
        table (str): Path to the table to update.
        missing_list (str): Path to the list of missing rows.
    """
    # Load data CVS sepparated with ";"
    df = pd.read_csv(table, sep=";")
        
    # Missing logs are in a txt file
    with open(missing_list) as f:
        missing_rows = f.readlines()
        # First row is the headder: eg. Patient_ID,Slide_ID,Slide,Missing_Stain
        # if "section" is not present in the header it is assumed to be "T01"
        header = missing_rows[0].split(",")
        if "section" not in missing_rows[0] :
            # skip the header
            missing_rows = missing_rows[1:]
            for row in missing_rows:
                row = row.split(",")
                patient_ID = row[0]
                slide_ID = row[1]
                slide = row[2]
                stain = row[3].strip()
                # the patient might be present in the table but the slide stain value is missing (we just want to to add the value "TRUE" to tha "stain" (eg. HE ...) column and patient row)
                
                mask = (df['patient_ID'].astype(str) == str(patient_ID)
                    ) & (
                        df['slide_ID'].astype(str) == str(slide_ID)
                    ) & (
                        df['section'].astype(str) == "T01"
                    ) & (
                        df['slide'].astype(str) == str(slide)
                    )
                
                                
                if not mask.any():
                    new_entry = pd.DataFrame({
                        "patient_ID": [patient_ID],
                        "slide_ID": [slide_ID],
                        "section": "T01",
                        "slide": [slide],
                        stain: ["ADDED AS A NEW ENTERY!!!!!!!"]
                    })
                    df = pd.concat([df, new_entry], ignore_index=True)
                
                # elif the patient exists and in its column "stain" the value is present ("True"): return "ou nou there is a value in this row" to the terminal
                elif df.loc[mask, stain].any():
                    print(f"Value already present in the table: {patient_ID}, {slide_ID}, {slide}, {stain}")
                
                else:
                    df.loc[mask, stain] = "MISSING SCAN!!!!!!!!!!"
        # save the updated table as a new table named output_csv
        df.to_csv(output_csv, index=False)
        print(f"Updated table saved to: {output_csv}")
        
        
# run
addMissingLog("/Users/terezajurickova/Desktop/bioimaging/manual_logs.csv", "/Users/terezajurickova/Desktop/bioimaging/missing_stains.txt")