from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseClass:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
