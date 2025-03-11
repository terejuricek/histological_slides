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
- **CSV Comparison**: The compareTables() function compares two CSV files and outputs the differences based on common columns (patient_ID, slide_ID, slide).


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
- ~~compareCSV: Compare two CSV files and output the differences.~~ -> to be changed to **compareTables**
  ```
  python histological_slide_processor.py compareTables <input_csv1> <input_csv2> [-t <output_txt>]
  ```
- compareStains: Compare two CSV files and output the differences in a txt file.
  ```
  python histological_slide_processor.py compareStains <input_csv1> <input_csv2> <output_txt>
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
- compareTables
- compareStains

## Order
orders **any .csv file** by user-inputed column (with the option of selecting another column to order the table by if values are reoccuring) </br>
```python
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
patient_ID  | slide_ID  | section | slide | >stain<
--- | --- | --- | --- |--- 
1 | SB-01 | NRM | 0 | True </br>


```python
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
  - add_row - created in order to reduce the redunancy within the main function -> <span style="color: red;">currently not working!</span>

</br>

## csv2excel and excel2csv
selfexplanatory - convertion between table formats </br>
```python
csv2excel(input_csv, output_excel)
excel2csv(input_excel, output_csv)
```
</br>

## compareTables
This function compares two cvs files for patient_ID and slide values.
It is made sesifically for the format of the original_table.csv whichs structure was discussed in the begining of this text. 
The needed criteria to run this function is thre presence of the given column names (patient_ID, slide) in both inputed files. </br>

<span style="color: royalblue;">Patient ID</span> | <span style="color: grey;">Slides ID</span> | <span style="color: royalblue;">Slides</span> | <span style="color: grey;">HE</span> | <span style="color: grey;">scan HE</span> | <span style="color: grey;">CD3</span> | <span style="color: grey;">scan CD3</span> | <span style="color: grey;">...</span>
| --- | --- | --- | --- | --- | --- | --- | --- 
| 1 |  | NRM 
| 1 |  | T01 

The output file will contain a list of patients that were not present in poth tables  </br>

```
compareTables(input_csv1, input_csv2, output_txt=None)
```
Arguments:
- <span style="color: royalblue;">input_csv1</span> -> file name of the first table
- <span style="color: royalblue;">input_csv2</span> -> file name of the second table
- <span style="color: royalblue;">output_txt</span> -> (optional)  text file used to store the output (messing patients), if not present as an argument, tatients are printed into the terminal

</br>

## compareStains
This function (similarly to the previouse one) compares two cvs files for patient_ID slide and <span style="color: steelblue;"> presence of stains</span> values. It is much more flexible and can manage various forms of the "original_table"

The needed criteria to run this function is the presence of the given column names (patient ID, slide ID, slide - their form can a little vary asshowcased later) in both inputed files. Also it is important to mention the difference in the other columns taht serve as stain logs:</br>

### Present stain scans table
- frormat created automaticly by previouse function **files2csv**
- expected to be in this exact format
- the only thing that can vary is the order of the columns
- <span style="color: lightcoral;">Note that the section column is not present in the original table</span>


<span style="color: royalblue;">patient_ID</span> | <span style="color: royalblue;">slide_ID</span> | <span style="color: grey;">section</span> | <span style="color: royalblue;">slide</span> | <span style="color: steelblue;"> HE</span> | <span style="color: steelblue;">CD3</span> | <span style="color: steelblue;">PD1</span> | <span style="color: grey;">...</span>
| --- | --- | --- | --- | --- | --- | --- | --- 
| 1 | SB-01 | NRM | 0 | True | True | 
| 1 | SB-01 | T01 | 1 | True |  | True
| 1 | SB-01 | T01 | 1 | True |  | 

### Original table
- there are various difference between versions and also to the automaticly created stain scans table
- below you can fin a version of the original table and also the solution within script that manages the inconsistency

<span style="color: royalblue;">Patient ID</span> | <span style="color: royalblue;">Slides ID</span> | <span style="color: royalblue;">Slides</span> | <span style="color: steelblue;">HE</span> | <span style="color: grey;">scan HE</span> | <span style="color: steelblue;">CD3</span> | <span style="color: grey;">scan CD3</span> | <span style="color: grey;">...</span>
| --- | --- | --- | --- | --- | --- | --- | --- 
| 1 |  | NRM | 1 | | 0
| 1 |  | T01 | 1 | | 2

### <span style="color: lightcoral;">Acknowledgement of table inconsistencies</span>
! note that these spesific changes are unique to this function "compareStains"
- change in script means there is no permanent change to the inputed tables

original table | scans table | change in script | command
| --- | --- | --- | ----
Patient ID | patient_ID | PATIENT_ID | .columns.str.strip().str.upper() </br> .rename(columns={"PATIENT ID": "PATIENT_ID"})  
Slides ID | slide_ID | SLIDE_ID | .columns.str.strip().str.upper() </br> .rename(columns={"SLIDES ID": "SLIDE_ID"})
PD-L1 | PDL1 | PDL1 | .columns.str.strip().str.upper() </br> .rename(columns={"PD-L1": "PDL1"})
FoxP3 | FOXP3 | FOXP3 | .columns.str.strip().str.upper() </br>


```python
compareStains(original_csv, stored_csv, output_txt, missing=False, verbose=False)
```
Arguments:
- <span style="color: royalblue;">original_csv</span> -> file name of the first table
- <span style="color: royalblue;">stored_csv</span> -> file name of the second table
- <span style="color: royalblue;">output_txt</span> -> (optional) text file used to store the output (missing stain scans), if not present as an argument, the missing scans are printed in the te