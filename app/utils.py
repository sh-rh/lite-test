import os
import cv2

from app.core.config import settings


async def create_project_folder(project_id: str):
    path = os.path.join(settings.PROJECTS_PATH, project_id)
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


async def create_versions(source_filename: str) -> dict[str, str]:
    img = cv2.imread(source_filename)