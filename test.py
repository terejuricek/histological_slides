import pandas as pd

def compareCSV(input_csv1, input_csv2, output_txt=None, return_indexes=False):
    """Compares two CSV files and prints/stores (in a .txt file) the differences.
    If return_indexes=True, returns two lists of (patient_ID, slide) pairs that were not in both tables.
    """
    df1 = pd.read_csv(input_csv1)
    df2 = pd.read_csv(input_csv2)
    
    # Clean the data: strip whitespace and convert to appropriate types
    df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df2 = df2.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df1['patient_ID'] = pd.to_numeric(df1['patient_ID'])
    df1['slide'] = pd.to_numeric(df1['slide'])
    df2['patient_ID'] = pd.to_numeric(df2['patient_ID'])
    df2['slide'] = pd.to_numeric(df2['slide'])
    
    # Align the DataFrames based on the first three columns
    common_columns = ["patient_ID", "slide_ID", "slide"]
    df1_aligned = df1.set_index(common_columns)
    df2_aligned = df2.set_index(common_columns)
    
    # Find rows that are in df1 but not in df2
    diff1 = df1_aligned[~df1_aligned.index.isin(df2_aligned.index)].copy()
    diff1 = diff1.reset_index()[["patient_ID", "slide"]]
    
    # Find rows that are in df2 but not in df1
    diff2 = df2_aligned[~df2_aligned.index.isin(df1_aligned.index)].copy()
    diff2 = diff2.reset_index()[["patient_ID", "slide"]]
    
    if return_indexes:
        return diff1.values.tolist(), diff2.values.tolist()
    
    # Combine the differences for output
    diff1['status'] = f"Only in {input_csv1}"
    diff2['status'] = f"Only in {input_csv2}"
    differences = pd.concat([diff1, diff2])
    
    result = f"Differences:\n{differences.to_string(index=False)}"
    
    if output_txt:
        with open(output_txt, 'w') as file:
            file.write(result)
        print(f"Differences saved to {output_txt}")
    else:
        print(result)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two CSV files and find unique rows.")
    parser.add_argument("input_csv1", help="Path to the first CSV file")
    parser.add_argument("input_csv2", help="Path to the second CSV file")
    parser.add_argument("-o", "--output", help="Path to save the differences in a .txt file", default=None)
    parser.add_argument("-t", "--return_indexes", help="Return only indexes (patient_ID, slide pairs)", action="store_true")

    args = parser.parse_args()

    if args.return_indexes:
        indexes1, indexes2 = compareCSV(args.input_csv1, args.input_csv2, return_indexes=True)
        print("Indexes only in file1:", indexes1)
        print("Indexes only in file2:", indexes2)
    else:
        compareCSV(args.input_csv1, args.input_csv2, output_txt=args.output)