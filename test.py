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
        
compareTables("/Users/terezajurickova/Desktop/bioimaging/original_table.csv", "/Users/terezajurickova/Desktop/bioimaging/scans.csv", "/Users/terezajurickova/Desktop/bioimaging/missing_from_table2.csv", "/Users/terezajurickova/Desktop/bioimaging/missing_from_table1.csv")
