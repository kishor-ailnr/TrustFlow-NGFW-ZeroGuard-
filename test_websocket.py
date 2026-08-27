import asyncio
import json
import websockets


async def test():
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:

        data = {
            "flow_id": "FLOW-001",
            "trust_score": 20,
            "risk_score": 95
        }

        await websocket.send(json.dumps(data))

        response = await websocket.recv()

        print("WebSocket response:")
        print(response)


asyncio.run(test())