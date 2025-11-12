from backend.config import db
from datetime import datetime


class PlatformInfo(db.Model):
    __tablename__ = 'biz_platform_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    department_id = db.Column(db.BigInteger, primary_key=True)  # 部门id
    create_id = db.Column(db.BigInteger)
    platform_name = db.Column(db.String(255))  # 平台名称
    platform_summary = db.Column(db.Text)  # 平台概述
    department = db.Column(db.String(255))  # 所属部门
    belonging_department = db.Column(db.String(255))  # 所属处室
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class BelongSystem(db.Model):
    __tablename__ = 'biz_belong_system'

    id = db.Column(db.BigInteger, primary_key=True)
    system_name = db.Column(db.String(50))  # 应用系统名称
    department = db.Column(db.String(255))  # 所属部门
    belonging_department = db.Column(db.String(255))  # 所属处室
    system_summary = db.Column(db.Text)  # 系统概述
    run_status = db.Column(db.String(255))  # 运行状态
    network = db.Column(db.String(255))  # 网络状态
    build_unit = db.Column(db.String(255))  # 建设单位
    construction_unit = db.Column(db.String(255))  # 承建单位
    service_object = db.Column(db.String(255))  # 服务对象
    build_method = db.Column(db.String(255))  # 建设方式
    system_type = db.Column(db.String(255))  # 系统类型
    investment_total = db.Column(db.String(255))  # 总投资（万元）
    funds_source = db.Column(db.String(255))  # 资金来源
    devops_expenses = db.Column(db.String(255))  # 2023年运维经费（万元）
    person = db.Column(db.String(255))  # 填报人
    phone = db.Column(db.String(255))  # 联系人电话
    notes = db.Column(db.Text)  # 备注
    create_id = db.Column(db.BigInteger)  # 当前登录人id
    department_id = db.Column(db.BigInteger)  # 部门id
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class DatasourceInfo(db.Model):
    __tablename__ = 'biz_datasource_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    datasource_name = db.Column(db.String(255))  # 数据源名称
    database_type = db.Column(db.String(255))  # 数据库类型
    belonging_system_id = db.Column(db.BigInteger)  # 所属应用系统id
    belonging_system_department_id = db.Column(db.BigInteger)  # 所属应用系统部门id
    database_name = db.Column(db.String(255))  # 数据库名称
    database_address = db.Column(db.String(255))  # 数据库地址
    database_username = db.Column(db.String(255))  # 用户名
    database_password = db.Column(db.String(255))  # 密码
    schema_name = db.Column(db.String(255))  # schema名称
    status = db.Column(db.String(255))
    table_name = db.Column(db.String(255))
    create_id = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class TableInfo(db.Model):
    __tablename__ = 'biz_table_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(255))
    table_comment = db.Column(db.String(255))
    data_total = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger,
                              nullable=True)
    schedule_id = db.Column(db.BigInteger,
                            nullable=True)
    table_history_id = db.Column(db.BigInteger)
    is_delete = db.Column(db.Boolean, default=False)  # 是否删除
    data_storage = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class TableHistoryInfo(db.Model):
    __tablename__ = 'biz_table_history_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(255))
    table_comment = db.Column(db.String(255))
    data_total = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger, db.ForeignKey('biz_datasource_info.id', ondelete='CASCADE'),
                              nullable=True)
    schedule_execute_id = db.Column(db.BigInteger,
                                    nullable=True)
    table_history_id = db.Column(db.BigInteger)
    data_storage = db.Column(db.BigInteger)
    # is_delete = db.Column(db.Boolean, default=False)  # 是否删除
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))

class TableHistoryTemplateInfo(db.Model):
    __tablename__ = 'biz_table_history_template_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(255))
    table_comment = db.Column(db.String(255))
    data_total = db.Column(db.BigInteger)
    datasource_id = db.Column(db.BigInteger, db.ForeignKey('biz_datasource_info.id', ondelete='CASCADE'),
                              nullable=True)
    schedule_execute_id = db.Column(db.BigInteger,
                                    nullable=True)
    table_history_id = db.Column(db.BigInteger)
    field_count = db.Column(db.Integer)
    data_total_change = db.Column(db.Integer)
    change_status = db.Column(db.Integer) # 0 add 1 update 2 consistent
    # is_delete = db.Column(db.Boolean, default=False)  # 是否删除
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))

class FieldInfo(db.Model):
    __tablename__ = 'biz_field_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    table_info_id = db.Column(db.BigInteger, db.ForeignKey('biz_table_info.id', ondelete='CASCADE'),
                              nullable=True)  # 表id
    name = db.Column(db.String(255))  # 字段名称
    primary_keys = db.Column(db.Boolean, default=False)  # 是否为主键
    type = db.Column(db.String(255))  # 字段类型
    nullable = db.Column(db.Boolean, default=False)  # 是否为空
    default = db.Column(db.String(255))  # 默认值
    autoincrement = db.Column(db.Boolean, default=False)  # 是否为自增长
    comment = db.Column(db.String(4000))  # 字段注释
    is_delete = db.Column(db.Boolean, default=False)  # 是否删除
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class FieldHistoryInfo(db.Model):
    __tablename__ = 'biz_field_history_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    table_info_id = db.Column(db.BigInteger, db.ForeignKey('biz_table_history_info.id', ondelete='CASCADE'),
                              nullable=True)  # 表id
    name = db.Column(db.String(255))  # 字段名称
    primary_keys = db.Column(db.Boolean, default=False)  # 是否为主键
    type = db.Column(db.String(255))  # 字段类型
    nullable = db.Column(db.Boolean, default=False)  # 是否为空
    default = db.Column(db.String(255))  # 默认值
    autoincrement = db.Column(db.Boolean, default=False)  # 是否为自增长
    comment = db.Column(db.String(4000))  # 字段注释
    # is_delete = db.Column(db.Boolean, default=False)  # 是否删除
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class TableAssociationInfo(db.Model):
    __tablename__ = 'biz_table_association_info'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    datasource_id = db.Column(db.BigInteger, db.ForeignKey('biz_datasource_info.id', ondelete='CASCADE'),
                              nullable=True)
    constrained_table_id = db.Column(db.BigInteger, db.ForeignKey('biz_table_info.id', ondelete='CASCADE'),
                                     nullable=True)  # 信息资源目录表id
    referred_table_id = db.Column(db.BigInteger, db.ForeignKey('biz_table_info.id', ondelete='CASCADE'),
                                  nullable=True)  # 被关联信息资源目录表id
    constrained_table = db.Column(db.String(255))  # 信息资源目录表名称
    constrained_columns = db.Column(db.String(255))  # 信息资源目录表关联字段
    referred_table = db.Column(db.String(255))  # 被关联信息资源目录表名称
    referred_columns = db.Column(db.String(255))  # 被关联信息资源目录表关联字段
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class DatabaseChangeLog(db.Model):
    __tablename__ = 'biz_database_change_log'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    schedule_info_id = db.Column(db.BigInteger,
                                 nullable=True)
    table_info_id = db.Column(db.BigInteger, db.ForeignKey('biz_table_history_info.id', ondelete='CASCADE'),
                              nullable=True)  # 信息资源目录表id
    field_info_id = db.Column(db.BigInteger, db.ForeignKey('biz_field_history_info.id', ondelete='CASCADE'),
                              nullable=True)
    change_type = db.Column(db.Enum('table', 'field', name='change_type'))
    change_status = db.Column(db.String(255))
    change_field = db.Column(db.String(255))
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))


class DataResources(db.Model):
    __tablename__ = 'biz_data_resources'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    dept_id = db.Column(db.BigInteger)
    file_path = db.Column(db.String(255))
    file_name = db.Column(db.String(255))
    create_id = db.Column(db.BigInteger)
    update_id = db.Column(db.BigInteger)
    download_total = db.Column(db.BigInteger, default=0)
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))

class DataResourcesAuth(db.Model):
    __tablename__ = 'biz_data_resources_auth'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger)
    data_resources_id = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))

class DataResourcesDownloadLog(db.Model):
    __tablename__ = 'biz_data_resources_download_log'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger)
    data_resources_id = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()))
    update_time = db.Column(db.String(255), default=lambda: int(datetime.now().timestamp()),
                            onupdate=lambda: int(datetime.now().timestamp()))

