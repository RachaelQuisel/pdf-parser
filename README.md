# PDF Parser
A Python tool that extracts line items from construction estimate PDFs and formats them intoCSV files ready for import.

## Features
- Parses PDFs using [pdfplumber](https://github.com/jsvine/pdfplumber)
- Extracts:
  - Quantity
  - Unit
  - Description (line item name)
  - Unit Price
- Outputs two CSVs:
  - `monday_items.csv` → scopes of work
  - `monday_subitems.csv` → line items under each scope
