import asyncio
import json
import websockets
import redis


async def get_websocket_data():
    items = {}
    uri = "wss://fstream.binance.com/ws/!miniTicker@arr"
    redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            temp_items = json.loads(data)
            update = 0

            for temp in temp_items:
                symbol = temp["s"]
                price = temp["c"]

                if symbol not in items or items[symbol] != price:
                    items[symbol] = price
                    update += 1
                    redis_client.set(symbol, price)

            total_symbols = len(items)
            print(f"Total symbols: {total_symbols}, Updated symbols: {update}")
            print(items)


asyncio.run(get_websocket_data())
