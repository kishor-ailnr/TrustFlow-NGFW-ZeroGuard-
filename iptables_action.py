import subprocess

def block_ip(ip_address: str):
    """
    Adds a real iptables DROP rule for the given IP.
    Requires the process to have sudo/root privileges on Linux (WSL2 Ubuntu).
    """
    try:
        result = subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"[iptables] Blocked {ip_address}")
            return True
        else:
            print(f"[iptables] Failed to block {ip_address}: {result.stderr}")
            return False
    except Exception as e:
        print(f"[iptables] Exception: {e}")
        return False


def unblock_ip(ip_address: str):
    """
    Removes the DROP rule for the given IP (for demo reset/cleanup).
    """
    try:
        result = subprocess.run(
            ["sudo", "iptables", "-D", "INPUT", "-s", ip_address, "-j", "DROP"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"[iptables] Unblocked {ip_address}")
            return True
        else:
            print(f"[iptables] Failed to unblock {ip_address}: {result.stderr}")
            return False
    except Exception as e:
        print(f"[iptables] Exception: {e}")
        return False


def list_rules():
    """
    Returns current iptables rules as text — call this before/after
    a block action to show the live diff to the judge.
    """
    result = subprocess.run(
        ["sudo", "iptables", "-L", "-n", "--line-numbers"],
        capture_output=True, text=True, timeout=5
    )
    return result.stdout