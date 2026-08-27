# backend/redteam/perturb.py

import random

# Columns that correspond to timing in the CIC-IDS2017 schema
TIMING_COLS = [
    "Flow Duration", "Flow IAT Mean", "Flow IAT Std", "Flow IAT Max", "Flow IAT Min",
    "Fwd IAT Total", "Fwd IAT Mean", "Fwd IAT Std", "Fwd IAT Max", "Fwd IAT Min",
    "Bwd IAT Total", "Bwd IAT Mean", "Bwd IAT Std", "Bwd IAT Max", "Bwd IAT Min",
    "Active Mean", "Active Max", "Active Min", "Idle Mean", "Idle Max", "Idle Min"
]

# Columns that correspond to packet size in the CIC-IDS2017 schema
PACKET_SIZE_COLS = [
    "Total Length of Fwd Packets", "Fwd Packet Length Max", "Fwd Packet Length Min",
    "Fwd Packet Length Mean", "Fwd Packet Length Std", "Bwd Packet Length Max",
    "Bwd Packet Length Min", "Bwd Packet Length Mean", "Bwd Packet Length Std",
    "Min Packet Length", "Max Packet Length", "Packet Length Mean", "Packet Length Std",
    "Packet Length Variance", "Average Packet Size", "Subflow Fwd Bytes"
]

def apply_evasion_perturbation(flow_row):
    """
    Takes a flow row (dict or pandas Series) and returns a copy with:
      - Timing features jittered by a random +/- 5-15%
      - Packet-size features padded by a random +3-8%
    """
    is_series = hasattr(flow_row, "copy")
    perturbed = flow_row.copy() if is_series else dict(flow_row)
    
    # Apply timing jitter: random float between +/- 5-15%
    for col in TIMING_COLS:
        if col in perturbed:
            sign = 1 if random.random() < 0.5 else -1
            magnitude = random.uniform(0.05, 0.15)
            factor = 1.0 + (sign * magnitude)
            perturbed[col] = perturbed[col] * factor
            
    # Apply packet size padding: random float between +3-8% (always positive padding)
    for col in PACKET_SIZE_COLS:
        if col in perturbed:
            factor = 1.0 + random.uniform(0.03, 0.08)
            perturbed[col] = perturbed[col] * factor
            
    return perturbed
