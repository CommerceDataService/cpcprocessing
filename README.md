# cpcprocessing

This repository contains a simple script (`processpcpfiles.py`) that will process cpc definition XML files.  These files can be obtained from:
http://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/Bulk.html
specifically from the section on the page labeled `CPC Definitions in XML format`.

In order to process the files, each unzipped and downloaded folder from the above page should be placed in the `xml_files` directory.  The script will then run through each folder within that directory and for each XML file, it will check if a CSV version already exists.  If it does not, the script will extract each CPC (Cooperative Patent Classification) code from the file, along with the title, informative references, special rules of classification, and glossary of terms.  The script also separates any CPC codes that are referenced within these sections (separated by a |).

The output file will be placed within the folder of the original file.  It will use the filename and extract the last part of the file name (the CPC code) for the CSV file.

Example: `cpc-definition-A01B.xml` -> `A01B.csv`
