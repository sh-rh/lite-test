from io import BytesIO
from PIL import Image


async def image_resize(file_obj: bytes, height: int = None, width: int = None):
    image = Image.open(BytesIO(file_obj))

    if height and width:
        resized = image.copy()
        resized.thumbnail((width, height))
        image_bytes = BytesIO()
        resized.save(image_bytes, format='JPEG')
        return image_bytes.getvalue()

    return file_obj
