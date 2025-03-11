# Original table
- name: 'slidy histo.xlsx'
- header: 'Patient ID'	'Slides ID'	'Slides'	'HE'	'scan HE'	'CD3'	''	'CD8'	''	'FoxP3'	''	'PD1'	''	'PD-L1'	''	'CAIX'	''	'CD68'	''	'CD45RO'	''

!!!! inconsistency with the naming in slidy histo.xlsx and ihc.txt of these stains:
slidy histo.xlsx    ihc.txt
FoxP3               FOXP3
PD-L1               PDL1

conpensation in script:
def compareCSVstains
...
    if stain == "FoxP3":
        stain = "FOXP3"
    elif stain == "PD-L1":
        stain = "PDL1"
...


# Table
### <span style="color: lightcoral;">Acknowledgement of table inconsistencies</span>
! note that these spesific changes are unique to this function "compareStains"
- change in script means there is no permanent change to the inputed tables

original table | scans table | change in script | command
| --- | --- | --- | ----
Patient ID | patient_ID | PATIENT_ID | .columns.str.strip().str.upper() </br> .rename(columns={"PATIENT ID": "PATIENT_ID"})  
Slides ID | slide_ID | SLIDE_ID | .columns.str.strip().str.upper() </br> .rename(columns={"SLIDES ID": "SLIDE_ID"})
PD-L1 | PDL1 | PDL1 | .columns.str.strip().str.upper() </br> .rename(columns={"PD-L1": "PDL1"})
FoxP3 | FOXP3 | FOXP3 | .columns.str.strip().str.upper() </br>

</br>

# Stain scans table
<span style="color: royalblue;">patient_ID</span> | <span style="color: royalblue;">slide_ID</span> | <span style="color: grey;">section</span> | <span style="color: royalblue;">slide</span> | <span style="color: steelblue;"> HE</span> | <span style="color: steelblue;">CD3</span> | <span style="color: steelblue;">PD1</span> | <span style="color: grey;">...</span>
| --- | --- | --- | --- | --- | --- | --- | --- 
| 1 | SB-01 | NRM | 0 | True | True | 
| 1 | SB-01 | T01 | 1 | True |  | True
| 1 | SB-01 | T01 | 1 | True |  | 

</br>

# Missing patients
## Only in ./scans.csv
```
 patient_ID slide_ID  slide
          1    SB-01      0
          2    SB-02      0
          4    SB-04      0
          7    SB-07      0
          9    SB-09      0
         11    SB-11      0
         14    SB-14      0
         17    SB-17      0
         18    SB-18      0
         18    SB-18      7
         20    SB-20      0
         21    SB-21      0
         22    SB-22      0
         28    SB-28      0
         40    SB-40      0
         42    SB-42      0
         43    SB-43      0
         45    SB-45      0
         46    SB-46      1
         52    SB-52      0
         53    SB-53      0
         57    SB-57      0
         64    SB-64      8
         68    SB-68      0
         70    SB-70      0
         71    SB-71      0
         77    SB-77      0
         93    SB-93     23
        119   SB-119     13
        123   SB-123      8
        135   SB-135      5
        136   SB-136      3
        142   SB-142     15
        142   SB-142      7
        158   SB-158      7
        174   SB-174     13
        186   SB-186      5
        203   SB-203      1
        203   SB-203     14
        203   SB-203      2
        203   SB-203     23
        212   SB-212      1
        212   SB-212     10
        212   SB-212     11
        220   SB-220      7
        226   SB-226      3
```
## Only in ./original_table.csv
```
         47    SB-47      8
         47    SB-47      9
         47    SB-47     10
         47    SB-47     11
         56    SB-56      7
         56    SB-56      9
         56    SB-56     10
         91    SB-91      3
         95    SB-95      1
        142 SB-142-A     14
        142 SB-142-A     16
        142 SB-142-A     13
        142 SB-142-1     15
        142 SB-142-B      8
        142 SB-142-B      9
        142 SB-142-B     11
        142 SB-142-2      7
        179   SB-179      5
        188   SB-188      3
        188   SB-188      5
        188   SB-188      6
        189   SB-189      3
        203 SB-203-1     10
        203 SB-203-1      8
        203 SB-203-1     14
        203 SB-203-1      7
        203 SB-203-2     10
        203 SB-203-2     17
        203 SB-203-2     24
        203 SB-203-2     23
        203 SB-203-2     20
        212 SB-212-1      4
        212 SB-212-1      6
        212 SB-212-1      8
        212 SB-212-1     10
        212 SB-212-2     12
        212 SB-212-2     13
        212 SB-212-2     11
```