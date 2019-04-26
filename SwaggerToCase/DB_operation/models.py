from sqlalchemy import Column, Integer, UniqueConstraint, Index, CHAR, VARCHAR, SmallInteger, PrimaryKeyConstraint, \
    ForeignKeyConstraint, TEXT

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False, comment="项目名称")
    desc = Column(VARCHAR(100), nullable=False, comment="简要介绍")
    owner = Column(VARCHAR(20), nullable=False, comment="创建人")

    __table_args__ = (
        PrimaryKeyConstraint("id"),  # primary key(id)
        UniqueConstraint('name', name='unique_name')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (Project.__name__, self.name, self.owner)


class TestCase(Base):
    __tablename__ = 'testcase'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False, comment="用例名称")
    # length = Column(SmallInteger, default=1, comment="API个数")
    project_id = Column(Integer, nullable=False, comment="project外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint('name', name='unique_name'),
        ForeignKeyConstraint(('project_id',), ('project.id',), name='fk_testcase_project')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (TestCase.__name__, self.id, self.name)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    body = Column(TEXT, nullable=False, comment="Config 主体信息")
    testcase_id = Column(Integer, nullable=False, comment="testcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('testcase_id',), ('testcase.id',), name='fk_config_testcase')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (Config.__name__, self.id, self.name)


class Parameters(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, nullable=False, autoincrement=True)
    key = Column(VARCHAR(100), nullable=False, comment="变量名")
    value = Column(VARCHAR(100), nullable=False, comment="参数驱动数据，默认来自于debugtalk")
    config_id = Column(Integer, nullable=False, comment="config外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('config_id',), ('config.id',), name='fk_parameters_config')
    )

    def __repr__(self):
        return "<class %s %s-%s-%s>" % (Extract.__name__, self.id, self.key, self.value)


class StepCase(Base):
    __tablename__ = 'stepcase'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    step = Column(Integer, nullable=False, default=1, comment="顺序")
    api_name = Column(VARCHAR(100), nullable=False)
    body = Column(TEXT, nullable=False, comment="StepCase 主体信息")
    testcase_id = Column(Integer, nullable=False, comment="testcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('testcase_id',), ('testcase.id',), name='fk_stepcase_testcase')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (StepCase.__name__, self.id, self.name)


class API(Base):
    __tablename__ = 'api'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    url = Column(VARCHAR(100), nullable=False, comment="请求地址")
    method = Column(VARCHAR(100), nullable=False, comment="请求方式")
    body = Column(TEXT, nullable=False, comment="API 主体信息")
    stepcase_id = Column(Integer, nullable=False, comment="stepcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('stepcase_id',), ('stepcase.id',), name='fk_api_stepcase')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (API.__name__, self.id, self.name)


class Validate(Base):
    __tablename__ = 'validate'
    id = Column(Integer, nullable=False, autoincrement=True)
    comparator = Column(VARCHAR(100), nullable=False)
    check = Column(VARCHAR(100), nullable=False, comment="请求地址")
    expected = Column(VARCHAR(100), nullable=False, comment="请求方式")
    stepcase_id = Column(Integer, nullable=False, comment="stepcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('stepcase_id',), ('stepcase.id',), name='fk_validate_stepcase')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (Validate.__name__, self.id, self.comparator)


class Extract(Base):
    __tablename__ = 'extract'
    id = Column(Integer, nullable=False, autoincrement=True)
    key = Column(VARCHAR(100), nullable=False, comment="引用变量")
    value = Column(VARCHAR(100), nullable=False, comment="被extract的字段")
    stepcase_id = Column(Integer, nullable=False, comment="stepcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('stepcase_id',), ('stepcase.id',), name='fk_extract_stepcase')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (Extract.__name__, self.id, self.key)

# class Report(Base):
#     pass
