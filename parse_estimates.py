import pdfplumber
import pandas as pd
import glob
import re
import os
from pathlib import Path

# Configuration
PATTERNS = [
    # Handles decimal/integer quantities with various units and optional total
    r'^(\d+(?:\.\d+)?)\s+(\w+)\s+(.+?)\s+\$([\d,]+\.?\d*)(?:\s+\$[\d,]+\.?\d*)?\s*$',
]
SKIP_WORDS = ["byrne construction", "proposal", "estimate", "project", "scope", "san antonio", "page", "date"]
STOP_WORDS = ["scope of work includes:", "total", "subtotal", "estimate total"]

def process_pdf(pdf_path):
    """Extract items and subitems from a single PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return [], []
    
    if not text.strip():
        return [], []
    
    lines = text.splitlines()
    base_name = os.path.basename(pdf_path)  # Cross-platform path handling
    
    # Extract group name
    group_match = re.search(r"BYRNE CONSTRUCTION SERVICES.*?EST\d+", text, re.DOTALL | re.IGNORECASE)
    group = re.sub(r'\s+', ' ', group_match.group(0)).strip() if group_match else f"Byrne Construction Services - {base_name}"
    
    items, subitems = [], []
    
    # Find scope sections
    for i, line in enumerate(lines):
        if "the scope of work includes:" not in line.lower():  # Case-insensitive
            continue
            
        # Find item name (look backwards)
        item_name = None
        for j in range(1, min(6, i+1)):
            candidate = lines[i-j].strip()
            if candidate and not any(word in candidate.lower() for word in SKIP_WORDS):
                # Clean item name - remove prices and parenthetical content
                item_name = re.sub(r"[\$][\d,]+\.?\d*|\(.*?\)", "", candidate).strip()
                if len(item_name) > 3:
                    break
        
        if not item_name:
            continue
            
        # Record item
        items.append({"Group": group, "Item": item_name, "Source PDF": base_name})
        
        # Extract subitems
        for line_idx in range(i+1, len(lines)):
            line = lines[line_idx].strip()
            
            # Stop conditions
            if not line or any(word in line.lower() for word in STOP_WORDS):
                break

            # Try to match patterns
            for pattern in PATTERNS:
                match = re.match(pattern, line)
                if match:
                    description = match.group(3).strip()
                    if len(description) > 2:  # Valid description
                        unit = match.group(2).upper()
                        # Normalize common unit variations
                        if unit in ['EACH', 'EA']:
                            unit = 'EACH'
                        
                        subitems.append({
                            "Item": item_name,
                            "Subitem": description,
                            "Quantity": match.group(1),
                            "Unit": unit,
                            "Unit Price": match.group(4).replace(',', ''),
                            "Group": group,
                            "Source PDF": base_name
                        })
                        break
    
    return items, subitems  # FIXED: Moved outside the loops

def main():
    """Main execution function."""
    # Find all PDFs
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    
    all_items, all_subitems = [], []
    
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        items, subitems = process_pdf(pdf_path)
        all_items.extend(items)
        all_subitems.extend(subitems)
        print(f"  - Found {len(items)} items with {len(subitems)} subitems")
    
    # Save results
    os.makedirs("output", exist_ok=True)
    
    if all_items:
        df_items = pd.DataFrame(all_items).drop_duplicates()
        df_items.to_csv("output/monday_items.csv", index=False)
        print(f"\nSaved {len(df_items)} unique items to output/monday_items.csv")
    else:
        print("\nNo items found to save.")
    
    if all_subitems:
        df_subitems = pd.DataFrame(all_subitems)
        df_subitems.to_csv("output/monday_subitems.csv", index=False)
        print(f"Saved {len(df_subitems)} subitems to output/monday_subitems.csv")
    else:
        print("No subitems found to save.")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()