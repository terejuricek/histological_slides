import pandas as pd
import argparse

# input file has to be a txt file with the list of files:
def process_fileNames(colouring: str, input_file: str, output_file: str):
    data = []
    skipped = []
    
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip() # remove leading and end whitespaces
            if line.endswith(".mrxs"):
                # SB236-T01-04-HE.mrxs 
                scanName = line
                # remove .mrxs
                line = line[:-5]
                slide_ID, section, slide = line.split("-")[:3]
                data.append([int(slide_ID[2:]), slide_ID, section, int(slide), scanName, True])
                    
            else:
                skipped.append(line)
    df = pd.DataFrame(data, columns=['patient_ID', 'slide_ID', 'section', 'slide', 'scanName', colouring])
    df.to_excel(output_file, index=False)
    print("Skipped files:")
    print(skipped)
    print("Output file: ", output_file)
    
def add_files(input_file: str, output_file: str):
    try:
        df = pd.read_excel(output_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["patient_ID", "slide_ID", "section", "slide", "scanName"])  # Empty DF

    new_data = []
    skipped = []
    
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.endswith(".mrxs"):
                scan_name = line
                line = line[:-5]  # Remove ".mrxs"
                
                # Extract parts: "SB236-T01-04-HE" -> ["SB236", "T01", "04", "HE"]
                parts = line.split("-")
                if len(parts) < 4:
                    skipped.append(scan_name)  # Skip malformed entries
                    continue
                
                slide_ID, section, slide, colouring = parts[:4]
                patient_ID = slide_ID[2:]  # Remove 'SB' prefix (e.g., "SB236" -> "236")

                # Convert all keys to string for uniform comparison
                new_entry = {
                    "patient_ID": int(patient_ID),
                    "slide_ID": str(slide_ID),
                    "section": str(section),
                    "slide": int(slide),
                    "scanName": str(scan_name),
                    colouring: True  # Mark this staining method
                }

                # Normalize the existing DataFrame (ensure all are strings for comparison)
                df = df.astype(str)

                # Check if the row already exists (excluding scanName)
                existing_row = df[
                    (df["patient_ID"] == new_entry["patient_ID"]) &
                    (df["slide_ID"] == new_entry["slide_ID"]) &
                    (df["section"] == new_entry["section"]) &
                    (df["slide"] == new_entry["slide"])
                ]

                if not existing_row.empty:
                    # Update existing row with new staining method
                    row_index = existing_row.index[0]
                    df.at[row_index, colouring] = True
                else:
                    # Append new entry
                    new_data.append(new_entry)

    # Convert new data into DataFrame and merge
    if new_data:
        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)

    # Ensure all staining method columns are present and fill NaN values with False
    staining_cols = [col for col in df.columns if col not in ["patient_ID", "slide_ID", "section", "slide", "scanName"]]
    for col in staining_cols:
        df[col] = df[col].fillna(False).astype(bool)

    # Save updated Excel file
    df.to_excel(output_file, index=False)
    
    print(f"Updated table saved to {output_file}")
    if skipped:
        print(f"Skipped {len(skipped)} malformed entries: {skipped}")

                


    
def main():
    parsers = argparse.ArgumentParser()
        # parsers variable in simple terms is a parser object 
    subparsers = parsers.add_subparsers(dest='command')
        # subparsers is a subparser object of parsers
        # command will store the subparser name
    
    parser_process_fileNames = subparsers.add_parser('process_fileNames', help='Sort list of file names in an .txt file to an excel table')
    parser_process_fileNames.add_argument('colouring', help='colour type')
    parser_process_fileNames.add_argument('input_file', help='input file')
    parser_process_fileNames.add_argument('output_file', help='output file')

    parser_process_add_files = subparsers.add_parser('add_files', help='Sort list of file names in an .txt file to an excel table')
    parser_process_add_files.add_argument('input_file', help='input file')
    parser_process_add_files.add_argument('output_file', help='output file')
    
    arguments = parsers.parse_args()
    
    if arguments.command == 'process_fileNames':
        process_fileNames(arguments.colouring , arguments.input_file, arguments.output_file)
    if arguments.command == 'add_files':
        add_files(arguments.input_file, arguments.output_file)
    


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python process_he.py <input_file> <output_file>")
#         sys.exit(1)

#     input_file = sys.argv[1]
#     output_file = sys.argv[2]
#     process_scans(input_file, output_file)

