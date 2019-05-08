from backend.models.models import Base
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:ate.sqa@127.0.0.1:3306/swagger?charset=utf8", encoding='utf-8', echo=True, max_overflow=5)


def init_db():
    # 获取继承于Base的所有表类进行创建
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    init_db()
    # drop_db()
