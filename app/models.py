from sqlmodel import Field, Relationship, SQLModel


class ProjectBase(SQLModel):
    pass


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    images: list['Image'] = Relationship(
        back_populates="project", sa_relationship_kwargs={'lazy': 'selectin'})


class ProjectPublic(ProjectBase):
    id: int
    image_count: int = 0


class ProjectsPublic(SQLModel):
    projects: list['ProjectPublic']


class VersionsBase(SQLModel):
    original: str
    thumb: str
    big_thumb: str
    big_1920: str
    d2500: str


class VersionsCreate(VersionsBase):
    pass


class Versions(VersionsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    images: 'Image' = Relationship(back_populates='versions')


class VersionsPublic(SQLModel):
    original: str
    thumb: str
    big_thumb: str
    big_1920: str
    d2500: str


class ImageBase(SQLModel):
    file_name: str = Field(unique=True, index=True)


class ImageCreate(ImageBase):
    project_id: int


class Image(ImageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    state: str

    project_id: int | None = Field(
        default=None, foreign_key='project.id', nullable=False)
    project: Project | None = Relationship(back_populates="images")

    versions_id: int | None = Field(
        default=None, foreign_key='versions.id')
    versions: Versions | None = Relationship(
        back_populates="images", sa_relationship_kwargs={'lazy': 'selectin'})


class ImagePublic(SQLModel):
    id: int
    state: str
    project_id: int
    versions: VersionsPublic


class ImagesPublic(SQLModel):
    images: list['ImagePublic']
