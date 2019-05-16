from backend.models.models import Base
from backend.models.curd import engine


def init_db():
    # 获取继承于Base的所有表类进行创建
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    init_db()
    # drop_db()
