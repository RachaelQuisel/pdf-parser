PDF Parser
A Python tool that extracts line items from construction estimate PDFs and formats them into CSV files ready for import.

How it Works
Regex-driven parsing: the script uses regex patterns to capture specific items in lines without skipping.
Pattern detection: it looks for a consistent structure — a number (quantity), a unit (hours, days, each, etc.), a description (the work or service), a unit price — and extracts them accurately.
Noise filtering: headers, totals, and irrelevant lines are automatically skipped.
