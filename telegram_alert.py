import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_alert(flow_id: str, action: str, risk_score: float, trust_score: float, reason: str):
    """
    Fires a real Telegram alert when the decision engine issues Block or Quarantine.
    """
    if action not in ("BLOCK", "QUARANTINE"):
        return None

    emoji = "🔴" if action == "BLOCK" else "🟠"
    message = (
        f"{emoji} *{action} TRIGGERED*\n"
        f"Flow ID: `{flow_id}`\n"
        f"Risk Score: `{risk_score:.3f}`\n"
        f"Trust Score: `{trust_score:.3f}`\n"
        f"Reason: {reason}"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        resp = requests.post(TELEGRAM_API_URL, data=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[Telegram alert failed] {e}")
        return None

import httpx

async def send_telegram_alert_async(flow_id, action, risk_score, trust_score, reason):
    if action not in ("BLOCK", "QUARANTINE"):
        return
    message = (
        f"{'🔴' if action == 'BLOCK' else '🟠'} *{action} TRIGGERED*\n"
        f"Flow ID: `{flow_id}`\nRisk: `{risk_score:.3f}`  Trust: `{trust_score:.3f}`\n"
        f"Reason: {reason}"
    )
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            await client.post(TELEGRAM_API_URL, data=payload)
        except httpx.HTTPError as e:
            print(f"[Telegram async alert failed] {e}")