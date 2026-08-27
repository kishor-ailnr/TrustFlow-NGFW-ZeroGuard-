import asyncio
import json
import websockets

async def main():
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:
        payload = {
            "flow_id": "DEMO-QUARANTINE-002",
            "trust_score": 60,
            "risk_score": 80
        }

        print("Sending:", json.dumps(payload))

        await websocket.send(json.dumps(payload))

        response = await websocket.recv()

        print("Server response:")
        print(response)

asyncio.run(main())
