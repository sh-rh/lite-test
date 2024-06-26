from sqlmodel import SQLModel, Session, create_engine

from app.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session):
    SQLModel.metadata.create_all(engine)
