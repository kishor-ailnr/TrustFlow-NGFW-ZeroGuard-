# backend/test_agent_tools.py
import ollama

tools = [
    {
        "type": "function",
        "function": {
            "name": "block_flow",
            "description": "Block a network flow immediately due to high-confidence malicious activity.",
            "parameters": {
                "type": "object",
                "properties": {"reason": {"type": "string", "description": "Why this flow should be blocked"}},
                "required": ["reason"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "allow_flow",
            "description": "Allow a network flow to proceed normally, no action needed.",
            "parameters": {
                "type": "object",
                "properties": {"reason": {"type": "string", "description": "Why this flow is safe"}},
                "required": ["reason"],
            },
        },
    },
]

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a network security analyst. Decide whether to block or "
                                       "allow flows based on the evidence given. Always call exactly one tool."},
        {"role": "user", "content": "A flow has a risk score of 92/100, matches a known-malicious JA3 TLS "
                                     "fingerprint, and the session trust score is only 15/100. Decide what to do."},
    ],
    tools=tools,
)

tool_calls = response["message"].get("tool_calls")
if tool_calls:
    call = tool_calls[0]
    print(f"✅ Agent called tool: {call['function']['name']}")
    print(f"   Arguments: {call['function']['arguments']}")
else:
    print("⚠️ No tool call returned — model replied with plain text instead:")
    print(response["message"].get("content"))