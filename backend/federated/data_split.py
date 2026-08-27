# backend/federated/data_split.py

import os
import glob
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def main():
    print("=== Phase 6: Federated Threat Intelligence Mesh - Data Splitting ===")
    
    # 1. Locate files
    csv_files = glob.glob("data/*.csv")
    cic_files = [f for f in csv_files if "cicids2017" in f]
    if not cic_files:
        # Fallback to any non-replay csv files in data/
        cic_files = [f for f in csv_files if "replay" not in f]
        
    if not cic_files:
        raise FileNotFoundError("No CIC-IDS2017 CSV files found in data/")
        
    print(f"Loading data from: {cic_files}")
    dfs = []
    for f in cic_files:
        print(f"Reading {f}...")
        df_chunk = pd.read_csv(f, low_memory=False)
        dfs.append(df_chunk)
    df = pd.concat(dfs, ignore_index=True)
    print(f"Raw shape: {df.shape}")
    
    # 2. Clean columns
    df.columns = df.columns.str.strip()
    
    # 3. Drop NaN/inf
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    print(f"Shape after dropping NaNs and Infs: {df.shape}")
    
    # 4. Check label column
    label_col = "Attack Type"
    if label_col not in df.columns:
        if "Label" in df.columns:
            label_col = "Label"
        else:
            raise ValueError(f"Label column '{label_col}' not found.")
            
    # Encode label column
    print("Encoding labels...")
    le = LabelEncoder()
    df["label"] = le.fit_transform(df[label_col])
    
    # Only keep numeric columns + label
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "label" not in numeric_cols:
        numeric_cols.append("label")
    df_clean = df[numeric_cols]
    
    # Downsample to keep it performant (e.g. 50,000 rows is great for quick training)
    MAX_ROWS = 50000
    if len(df_clean) > MAX_ROWS:
        print(f"Downsampling to {MAX_ROWS} rows stratified by label...")
        df_clean, _ = train_test_split(
            df_clean,
            train_size=MAX_ROWS,
            stratify=df_clean["label"],
            random_state=42
        )
        df_clean = df_clean.reset_index(drop=True)
    
    # 5. Split by attack-type distribution (non-IID)
    # Shard A (Client 0) gets 75% of even label classes, 25% of odd label classes.
    # Shard B (Client 1) gets 25% of even label classes, 75% of odd label classes.
    # This ensures both clients have all classes, but highly skewed distributions!
    client_0_list = []
    client_1_list = []
    
    for label_val, group in df_clean.groupby("label"):
        n_samples = len(group)
        if n_samples < 2:
            # Put small groups in both or alternate
            if label_val % 2 == 0:
                client_0_list.append(group)
            else:
                client_1_list.append(group)
            continue
            
        if label_val % 2 == 0:
            frac = 0.75
        else:
            frac = 0.25
            
        c0 = group.sample(frac=frac, random_state=42)
        c1 = group.drop(c0.index)
        
        client_0_list.append(c0)
        client_1_list.append(c1)
        
    df_client_0 = pd.concat(client_0_list, ignore_index=True)
    df_client_1 = pd.concat(client_1_list, ignore_index=True)
    
    # Shuffle datasets
    df_client_0 = df_client_0.sample(frac=1.0, random_state=42).reset_index(drop=True)
    df_client_1 = df_client_1.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    print(f"Client 0 dataset shape: {df_client_0.shape}")
    print(f"Client 1 dataset shape: {df_client_1.shape}")
    
    # Save the files
    os.makedirs("backend/federated/data", exist_ok=True)
    df_client_0.to_csv("backend/federated/data/client_0.csv", index=False)
    df_client_1.to_csv("backend/federated/data/client_1.csv", index=False)
    print("Successfully wrote client_0.csv and client_1.csv to backend/federated/data/")

if __name__ == "__main__":
    main()
