import subprocess

RULE_PREFIX = "TrustFlowNGFW_Block_"

def block_ip(ip: str) -> bool:
    rule_name = f"{RULE_PREFIX}{ip}"
    try:
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name={rule_name}", "dir=in", "action=block", f"remoteip={ip}"],
            check=True, capture_output=True, text=True, timeout=5,
        )
        print(f"[Firewall] Blocked {ip} (rule: {rule_name})")
        return True
    except Exception as e:
        print(f"[Firewall] Could not add rule for {ip} ({e}) - likely needs admin rights.")
        return False

def unblock_ip(ip: str) -> bool:
    try:
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={RULE_PREFIX}{ip}"],
            check=True, capture_output=True, text=True, timeout=5,
        )
        return True
    except Exception as e:
        print(f"[Firewall] Could not remove rule for {ip}: {e}")
        return False

def list_rules() -> str:
    try:
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
            capture_output=True, text=True, timeout=5,
        )
        lines = [l for l in result.stdout.splitlines() if RULE_PREFIX in l]
        return "\n".join(lines) if lines else "(no TrustFlow rules active)"
    except Exception as e:
        return f"(could not list rules: {e})"