# Histological slides data
This Python script handles tables with information about histological slides and scans. It allows users to:
* Parse filenames of histological scans to extract metadata such as patient ID, slide ID, section, slide number, and staining method.
* Update and create CSV files based on input text files.
* Convert between CSV and Excel file formats.
* Compare two CSV files to find and output the differences.

## Features
- **Filename Parsing**: The parse_filename() function extracts information from filenames in the format:
  ```
  <patient_ID>-<section>-<slide_number>-<stain_method>.mrxs
  ```
- **Order CSV**: The order() function sorts an existing CSV file by a specified column and saves the result.
- **Convert Files**:
  - **files2csv()** creates or updates a CSV file by adding data from a text file that contains filenames of histological scan slides.
	- **csv2excel()** converts a CSV file to an Excel file.
  - **excel2csv()** converts an Excel file back to a CSV file.
- **CSV Comparison**: The compareCSV() function compares two CSV files and outputs the differences based on common columns (patient_ID, slide_ID, slide).

## Instalation
Ensure you have the required Python version (>= 3.6) and install the necessary libraries:
  ```
  pip install pandas
  ```
  ```
  pip install argparse
  ```
  ```
  pip install os
  ```
## Usage

Command-Line Interface (CLI)

The script provides several commands to process histological slide data.

## Commands
- order: Sort the CSV file by the specified column.
  ```
  python histological_slide_processor.py order <output_csv> <column>
  ```
- files2csv: Create or update a CSV file from an input text file.
  ```
  python histological_slide_processor.py files2csv <input_txt> <output_csv>
  ```
- CVS and excel conversion
  - csv2excel: Convert a CSV file to an Excel file.
    ```
    python histological_slide_processor.py csv2excel <input_csv> <output_excel>
    ```
  - excel2csv: Convert an Excel file to a CSV file.
    ```
    python histological_slide_processor.py csv2excel <input_csv> <output_excel>
    ```
- ~~compareCSV: Compare two CSV files and output the differences.~~ -> to be changed to **compareCSVpatient**
  ```
  python histological_slide_processor.py compareCSVpatient <input_csv1> <input_csv2> [-t <output_txt>]
  ```
- compareCSVstains: Compare two CSV files and output the differences in a txt file.
  ```
  python histological_slide_processor.py compareCSVstains <input_csv1> <input_csv2> <output_txt>
  ```  

# Expected Original_table structure:
<span style="color: royalblue;">Patient ID</span> | <span style="color: royalblue;">Slides ID</span> | <span style="color: royalblue;">Slides</span> | <span style="color: pink;">HE</span> | <span style="color: grey;">scan HE</span> | <span style="color: pink;">CD3</span> | <span style="color: grey;">scan CD3</span> | <span style="color: pink;">CD8</span> | <span style="color: grey;">scan CD8</span> | <span style="color: pink;">FoxP3</span> | <span style="color: grey;">scan FoxP3</span> | <span style="color: pink;">PD1</span> | <span style="color: grey;">scan PD1</span> | <span style="color: pink;">PD-L1</span> | <span style="color: grey;">scan PD-L1</span> | <span style="color: pink;">CAIX</span> | <span style="color: grey;">scan CAIX</span> | <span style="color: pink;">CD68</span> | <span style="color: grey;">scan CD68</span> | <span style="color: pink;">CD45R</span> | <span style="color: grey;">scan CD45RO</span>
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |---
1 | SB-01 | 1 | 1 | yes | 1 | yes | 2 | yes | 1 | yes | 1 | yes | 1 | yes | 1 | yes | m | yes | 1 | yes
1 | SB-01 | 3 | 1 | yes | 1 | yes | 1 | yes | 2 | yes | 1 | yes | 2 | yes | 0 | no | 1 | yes | 1 | yes
...

- position of columns isnt important
- <span style="color: royalblue;">Blue column names</span> are nessecery in this exact phrasing
- <span style="color: pink;">Pink columns</span> are nessecery
-  <span style="color: grey;">Grey column names</span> are impartial to the otput

currently recognized staining methods: 
```
['HE', 'CD3', 'CD8', 'FoxP3', 'PD1', 'PD-L1', 'CAIX', 'CD68', 'CD45RO']
```
<span style="color: red;">to be changed:
addition of a function that adaptively gathers the wanted staining methods</span>

# Detailed eploration of each in-line command 
- order
- files2csv
- csv2excel
- excel2csv
- compareCSV
- compareCSVstains

## Order
orders **any .csv file** by user-inputed column (with the option of selecting another column to order the table by if values are reoccuring) </br>
```
order(output, column1, column2=None)
```
Arguments:
- <span style="color: royalblue;">output</span> -> file name of the file to order
- <span style="color: royalblue;">column1</span> -> the main columnb to order by
- <span style="color: royalblue;">column2</span> -> (optional) second column to order by

## files2csv
takes in a any .txt file containing scan file names in the following format: </br>
<span style="color: steelblue;"> *SB001-NRM-00-CD3.mrxs*  </br>
ID-section-slide-stain.mrxs </span> </br>
Which will be translated to the following: </br>
patient_ID	| slide_ID	| section	| slide | >stain<
--- | --- | --- | --- |--- 
1 | SB-01 | NRM | 0 | True </br>


```
files2csv(input_txt, output_csv)
```
Arguments:
- <span style="color: royalblue;">input_txt</span> -> .txt file containing scan file names with previously declared format
- <span style="color: royalblue;">output_csv</span> -> outputed .csv file which if:
  - *already exists* in the current directory, it will simply be updated, mantaining the already inputed rows
  - *is not present* in the currrent directory, will be created from scrach and thus after the command finishes, will contain only the scan logs from the current input_txt

corespondig functions:
- parse_filename - utilizes the extraction of information from filenames as previously demostrated and returns each as a string
- management of stains:
  - stain_check - sicne one scan can contin 1 or 2 tissuer slides, and thus 1 or 2 stains, this functions manages the correct addition of each to the cvs table. returnes extracted stains as a list (or a )
  - known_stains -> currently static function storing a set of known stains which upon call returnes boolem value representing presence or absence of the currently parsing stain in the known list
    - its presence as a separate function is currently indifferent to storing the stains directly in the previous function, however represents an *to be integrated* possibyility of adaptively reading/inputing the wanted stains
  - add_row - created in order to reduce the redunancy within the main function
    - <span style="color: red;">currently not working</span>

## csv2excel and excel2csv
selfexplanatory - convertion between table formats </br>
```
csv2excel(input_csv, output_excel)
excel2csv(input_excel, output_csv)
```

## compareCSV
This function compares two cvs files for patient_ID and slide values.
It is made sesifically for the format of the original_table.csv whichs structure was discussed in the begining og this text. 
The needed criteria to run this function is thre presence of the given column names (patient_ID, slide) in both inputed files.
Theese columns are present in and output a text file containing  </br>
```
compareCSV(input_csv1, input_csv2, output_txt=None)
```



<span style="color: royalblue;"></span>