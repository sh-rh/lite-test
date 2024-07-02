from io import BytesIO
from PIL import Image
from fastapi import WebSocket


async def image_resize(file_obj: bytes, width: int = None, height: int = None) -> bytes:
    image = Image.open(BytesIO(file_obj))

    if height and width:
        resized = image.copy()
        resized.thumbnail((width, height))
        image_bytes = BytesIO()
        resized.save(image_bytes, format='JPEG')
        return image_bytes.getvalue()

    return file_obj


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)