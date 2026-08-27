# backend/federated/run_federated_demo.py

import os
import sys
import subprocess
import time
import json

def get_python_executable():
    # Identify the python executable inside the venv
    if os.name == "nt":  # Windows
        venv_python = os.path.join("venv", "Scripts", "python.exe")
    else:  # Unix/macOS
        venv_python = os.path.join("venv", "bin", "python")
        
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def main():
    print("======================================================================")
    print("        STARTING FEDERATED THREAT INTELLIGENCE MESH DEMO")
    print("======================================================================\n")

    python_exe = get_python_executable()
    print(f"[Demo] Using Python executable: {python_exe}")

    # 1. Run Data Split
    print("\n--- Step 1: Splitting and Preprocessing CIC-IDS2017 Dataset ---")
    data_split_script = os.path.join("backend", "federated", "data_split.py")
    try:
        subprocess.run([python_exe, data_split_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[Demo] Error during data split: {e}")
        sys.exit(1)

    # 2. Start Flower Server
    print("\n--- Step 2: Starting Flower Server Subprocess ---")
    server_script = os.path.join("backend", "federated", "server.py")
    server_proc = subprocess.Popen(
        [python_exe, server_script],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    # Allow server to initialize and start listening on port 8080
    time.sleep(3)

    # 3. Start Clients
    print("\n--- Step 3: Starting Client Subprocesses ---")
    client_script = os.path.join("backend", "federated", "client.py")
    
    print("[Demo] Launching Client 0...")
    client0_proc = subprocess.Popen(
        [python_exe, client_script, "--client-id", "0"],
        stdout=subprocess.DEVNULL,  # Redirect client outputs to devnull to avoid cluttering
        stderr=sys.stderr
    )
    
    print("[Demo] Launching Client 1...")
    client1_proc = subprocess.Popen(
        [python_exe, client_script, "--client-id", "1"],
        stdout=subprocess.DEVNULL,
        stderr=sys.stderr
    )

    # 4. Wait for completion
    print("\n--- Step 4: Training Federated Model across 3 Rounds ---")
    print("[Demo] Waiting for clients to finish training...")
    try:
        # Wait for clients first
        client0_proc.wait(timeout=120)
        client1_proc.wait(timeout=120)
        print("[Demo] Both clients finished execution.")
    except subprocess.TimeoutExpired:
        print("[Demo] Timeout: Clients did not finish in 2 minutes. Terminating...")
        client0_proc.terminate()
        client1_proc.terminate()

    print("[Demo] Waiting for server to finish and export results...")
    try:
        server_proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        print("[Demo] Server process did not exit automatically. Terminating...")
        server_proc.terminate()

    # 5. Read and print logs
    print("\n--- Step 5: Final Evaluation Logs ---")
    log_path = os.path.join("backend", "federated", "results", "accuracy_log.json")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
        print("\n=== FEDERATED ACCURACY LOG ===")
        print(json.dumps(logs, indent=2))
        print("==============================\n")
    else:
        print(f"[Demo] Error: Accuracy log file not found at {log_path}!")

    print("======================================================================")
    print("                      DEMO RUN COMPLETE")
    print("======================================================================")

if __name__ == "__main__":
    main()
