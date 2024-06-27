from sqlmodel import Field, Relationship, SQLModel


class ProjectBase(SQLModel):
    pass


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    images: list['Image'] | None = Relationship(back_populates="project")


class ProjectPublic(ProjectBase):
    id: int


class ProjectsPublic(SQLModel):
    projects: list['ProjectPublic'] | None


class ImageBase(SQLModel):
    file_name: str | None = Field(unique=True, index=True)


class ImageCreate(ImageBase):
    project_id: int


class VersionsBase(SQLModel):
    original: str
    thumb: str
    big_thumb: str
    big_1920: str
    d2500: str


class Versions(VersionsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
class VersionPublic(VersionsBase):
    pass


class Image(ImageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    state: str

    project_id: int | None = Field(
        default=None, foreign_key='project.id', nullable=False)
    project: Project | None = Relationship(back_populates="images")

    version_id: int | None = Field(
        default=None, foreign_key='versions.id', nullable=False)
    versions: Versions | None = Relationship(back_populates="image")


class ImagePublic(SQLModel):
    id: int
    state: str
    project_id: int
    versions: VersionPublic


class ImagesPublic(SQLModel):
    images: list['ImagePublic']


class ProjectCreate(ProjectBase):
    image: Image
