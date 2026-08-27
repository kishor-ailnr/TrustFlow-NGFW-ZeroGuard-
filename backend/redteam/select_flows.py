# backend/redteam/select_flows.py

import os
import glob
import pandas as pd

def main():
    print("=== Phase 7: Adversarial Red-Teaming - Selecting Malicious Flows ===")
    
    # Locate files
    csv_files = glob.glob("data/*.csv")
    cic_files = [f for f in csv_files if "cicids2017" in f]
    if not cic_files:
        cic_files = [f for f in csv_files if "replay" not in f]
        
    if not cic_files:
        raise FileNotFoundError("No CIC-IDS2017 CSV files found in data/")
        
    target_csv = cic_files[0]
    print(f"Loading candidate malicious flows from {target_csv}...")
    
    # Load entire dataset since we need specific indices
    df = pd.read_csv(target_csv, low_memory=False)
    df.columns = df.columns.str.strip()
    
    # We want a mix of robust attacks (always caught) and evadable ones
    robust_indices = [1496, 35292, 37697, 37698]
    evadable_indices = [157230, 182154, 182224, 182677]
    
    selected_indices = robust_indices + evadable_indices
    sample_df = df.iloc[selected_indices].copy()
    
    # Ensure data directory exists
    os.makedirs("backend/redteam/data", exist_ok=True)
    
    # Save the selected malicious flows
    output_path = "backend/redteam/data/malicious_sample.csv"
    sample_df.to_csv(output_path, index=False)
    print(f"Successfully saved {len(sample_df)} malicious flow rows to {output_path}")

if __name__ == "__main__":
    main()

