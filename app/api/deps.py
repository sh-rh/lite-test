from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
