# PDF Parser
## A Python tool that extracts line items from construction estimate PDFs and formats them into CSV files ready for import.

## How it Works
Regex-driven parsing: the script scans PDF text and breaks it into lines for processing. It recognizes patterns to capture specific items in lines without skipping. Ignores noise like headers, totals, blank lines, or anything that doesn’t match the pattern. It looks for a consistent structure, (including numbers (quantity), units (hours, days, each, etc.), descriptions (the work or service), prices), and extracts them accurately. Irrelevant lines are skipped with a built in false safe to note skipped lines.
