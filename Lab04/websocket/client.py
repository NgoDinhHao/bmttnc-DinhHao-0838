import tornado.ioloop
import tornado.websocket
import asyncio

class WebSocketClient:
    def __init__(self):
        self.connection = None

    async def start(self):
        while True:
            try:
                print("Connecting to server...")
                self.connection = await tornado.websocket.websocket_connect(
                    "ws://localhost:8888/websocket/",
                    ping_interval=10,
                    ping_timeout=30,
                )
                print("Connected! Listening for messages...")
                await self.read_messages()
            except Exception as e:
                print(f"Connection error: {e}")
                print("Reconnecting in 3 seconds...")
                await asyncio.sleep(3)

    async def read_messages(self):
        while True:
            try:
                message = await self.connection.read_message()
                if message is None:
                    print("Server closed connection. Reconnecting...")
                    break
                print(f"Received message: {message}")
            except Exception as e:
                print(f"Read error: {e}")
                break

def main():
    client = WebSocketClient()
    asyncio.get_event_loop().run_until_complete(client.start())

if __name__ == "__main__":
    main()
