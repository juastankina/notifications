import asyncio
import logging

import websockets

CLIENTS = set()

logging.basicConfig(level=logging.INFO)


class Messages:
    messages: list = []

    def add_message(self, message):
        self.messages.append(message)

    def del_message(self, message):
        self.messages.remove(message)

    def get_messages(self):
        return self.messages


class WSServer:

    def __init__(self):
        self.messages: Messages = Messages()

    async def init(self, websocket: websockets.WebSocketServerProtocol) -> None:
        CLIENTS.add(websocket)

    async def disconnect(self, websocket: websockets.WebSocketServerProtocol) -> None:

        CLIENTS.remove(websocket)

    async def send_message(self, message: str):
        if CLIENTS:
            await asyncio.wait([asyncio.create_task(client.send(message)) for client in CLIENTS])

    async def produce(self) -> None:
        for message in self.messages.get_messages():
            await self.send_message(message)
        self.messages.messages.clear()

    async def ws_handler(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        logging.info('Установление соединения')
        await self.init(websocket)
        try:
            await self.produce()
        finally:
            await self.disconnect(websocket)


if __name__ == '__main__':

    logging.info('Запуск websocket-сервера')
    server = WSServer()
    start_server = websockets.serve(server.ws_handler, "localhost", 8765)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
