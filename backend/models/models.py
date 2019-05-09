from sqlalchemy import Column, Integer, UniqueConstraint, Index, CHAR, VARCHAR, SmallInteger, PrimaryKeyConstraint, \
    ForeignKeyConstraint, TEXT
from backend.models.compress import CompressField
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from passlib.apps import custom_app_context as pwd_context


class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, nullable=False, autoincrement=True)
    username = Column(VARCHAR(100), nullable=False)
    password = Column(TEXT, nullable=False)
    email = Column(VARCHAR(100), nullable=False)

    def hash_password(self, password):  # 给密码加密方法
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):  # 验证密码方法
        return pwd_context.verify(password, self.password)

    __table_args__ = (
        PrimaryKeyConstraint("id"),  # primary key(id)
        UniqueConstraint('username', name='unique_username')
    )


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False, comment="项目名称")
    mode = Column(VARCHAR(20), nullable=False, comment="创建方式")
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
        # UniqueConstraint('name', name='unique_name'),  # 同名没关系，属于不同project就行
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
    value_type = Column(VARCHAR(50), nullable=False, comment="指定参数列表、csv表格还是自定义函数")
    config_id = Column(Integer, nullable=False, comment="config外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('config_id',), ('config.id',), name='fk_parameters_config')
    )

    def __repr__(self):
        return "<class %s %s-%s-%s>" % (Extract.__name__, self.id, self.key, self.value)


class VariablesGlobal(Base):
    __tablename__ = 'variables_global'
    id = Column(Integer, nullable=False, autoincrement=True)
    key = Column(VARCHAR(100), nullable=False, comment="变量名")
    value = Column(TEXT, nullable=False, comment="变量值")  # 注意：这里与parameters的不同，需要json库转换
    config_id = Column(Integer, nullable=False, comment="config外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('config_id',), ('config.id',), name='fk_varGlobal_config')
    )

    def __repr__(self):
        return "<class %s %s-%s-%s>" % (Extract.__name__, self.id, self.key, self.value)


class StepCase(Base):
    __tablename__ = 'stepcase'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    step = Column(Integer, nullable=False, default=1, comment="顺序")
    api_name = Column(VARCHAR(100), nullable=False)  # ToDO: 建立唯一键
    body = Column(TEXT, nullable=False, comment="StepCase 主体信息")
    testcase_id = Column(Integer, nullable=False, comment="testcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('testcase_id',), ('testcase.id',), name='fk_stepcase_testcase')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (StepCase.__name__, self.id, self.name)


class VariablesLocal(Base):
    __tablename__ = 'variables_local'
    id = Column(Integer, nullable=False, autoincrement=True)
    key = Column(VARCHAR(100), nullable=False, comment="变量名")
    value = Column(TEXT, nullable=False, comment="变量值")
    stepcase_id = Column(Integer, nullable=False, comment="stepcase外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('stepcase_id',), ('stepcase.id',), name='fk_varLocal_stepcase')
    )

    def __repr__(self):
        return "<class %s %s-%s-%s>" % (Extract.__name__, self.id, self.key, self.value)


class Validate(Base):
    __tablename__ = 'validate'
    id = Column(Integer, nullable=False, autoincrement=True)
    comparator = Column(VARCHAR(100), nullable=False, comment="校验类型")
    check = Column(VARCHAR(100), nullable=False, comment="校验值")
    expected = Column(VARCHAR(100), nullable=False, comment="期望值")
    expected_type = Column(VARCHAR(100), nullable=False, comment="期望值类型")
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


class Report(Base):
    __tablename__ = 'report'

    id = Column(Integer, nullable=False, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False, comment="报告名称")
    current_time = Column(VARCHAR(100), nullable=False, comment="报告生成时间")
    render_content = Column(CompressField(9999999), nullable=False, comment="Html Code")
    tester = Column(VARCHAR(100), nullable=False, comment="测试人员")
    description = Column(VARCHAR(1000), nullable=False, comment="报告描述")
    project_id = Column(Integer, nullable=False, comment="project外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('project_id',), ('project.id',), name='fk_report_project')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (TestCase.__name__, self.id, self.name)


class VariablesEnv(Base):
    __tablename__ = 'variables_env'
    id = Column(Integer, nullable=False, autoincrement=True)
    key = Column(VARCHAR(100), nullable=False, comment="变量名")
    value = Column(TEXT, nullable=False, comment="变量值")
    project_id = Column(Integer, nullable=False, comment="project外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('project_id',), ('project.id',), name='fk_varEnv_project')
    )

    def __repr__(self):
        return "<class %s %s-%s-%s>" % (Extract.__name__, self.id, self.key, self.value)


class API(Base):
    __tablename__ = 'test_api'

    id = Column(Integer, nullable=False, autoincrement=True)
    api_func = Column(VARCHAR(100), nullable=False)
    url = Column(VARCHAR(100), nullable=False, comment="请求地址")
    method = Column(VARCHAR(100), nullable=False, comment="请求方式")
    body = Column(TEXT, nullable=False, comment="API 主体信息")
    project_id = Column(Integer, nullable=False, comment="project外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        # UniqueConstraint('name', name='unique_name'),  # 同名没关系，属于不同project就行
        ForeignKeyConstraint(('project_id',), ('project.id',), name='fk_testapi_project')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (API.__name__, self.id, self.api_func)


class DebugTalk(Base):
    __tablename__ = 'debugtalk'

    id = Column(Integer, nullable=False, autoincrement=True)
    code = Column(TEXT, nullable=False, comment="驱动代码")
    project_id = Column(Integer, nullable=False, comment="project外键")

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(('project_id',), ('project.id',), name='fk_debugtalk_project')
    )

    def __repr__(self):
        return "<class %s %s-%s>" % (API.__name__, self.id, self.project_id)
