from backend.config import db

class SysClient(db.Model):
    __tablename__ = 'sys_client'

    id = db.Column(db.BigInteger, primary_key=True)
    client_id = db.Column(db.String(64))
    client_key = db.Column(db.String(32))
    client_secret = db.Column(db.String(255))
    grant_type = db.Column(db.String(255))
    device_type = db.Column(db.String(32))
    active_timeout = db.Column(db.BigInteger)
    timeout = db.Column(db.BigInteger)
    status = db.Column(db.String(32))
    del_flag = db.Column(db.String(32))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(32))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(32))
    rollback_url = db.Column(db.String(2048))

class SysConfig(db.Model):
    __tablename__ = 'sys_config'

    config_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    config_name = db.Column(db.String(100))
    config_key = db.Column(db.String(100))
    config_value = db.Column(db.String(500))
    config_type = db.Column(db.String(32))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(32))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(32))
    remark = db.Column(db.String(500))

class SysDept(db.Model):
    __tablename__ = 'sys_dept'

    dept_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    parent_id = db.Column(db.BigInteger)
    ancestors = db.Column(db.String(500))
    dept_name = db.Column(db.String(30))
    order_num = db.Column(db.BigInteger)
    leader = db.Column(db.BigInteger)
    phone = db.Column(db.String(11))
    email = db.Column(db.String(50))
    status = db.Column(db.String(32))
    del_flag = db.Column(db.String(32))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    dept_code = db.Column(db.String(500))
    batch_name = db.Column(db.String(255))

class SysDictData(db.Model):
    __tablename__ = 'sys_dict_data'

    dict_code = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    dict_sort = db.Column(db.BigInteger)
    dict_label = db.Column(db.String(100))
    dict_value = db.Column(db.String(100))
    dict_type = db.Column(db.String(100))
    css_class = db.Column(db.String(100))
    list_class = db.Column(db.String(10))
    is_default = db.Column(db.String(50))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysDictType(db.Model):
    __tablename__ = 'sys_dict_type'

    dict_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    dict_name = db.Column(db.String(100))
    dict_type = db.Column(db.String(100))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysExternalApp(db.Model):
    __tablename__ = 'sys_external_app'

    app_name = db.Column(db.String(255))
    app_code = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    status = db.Column(db.String(100))
    create_time = db.Column(db.String(100))
    id = db.Column(db.BigInteger, primary_key=True)

class SysLogininfor(db.Model):
    __tablename__ = 'sys_logininfor'

    info_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    user_name = db.Column(db.String(50))
    client_key = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    ipaddr = db.Column(db.String(128))
    login_location = db.Column(db.String(255))
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    status = db.Column(db.String(32))
    msg = db.Column(db.String(255))
    login_time = db.Column(db.String(255))

class SysMenu(db.Model):
    __tablename__ = 'sys_menu'

    menu_id = db.Column(db.BigInteger, primary_key=True)
    menu_name = db.Column(db.String(50))
    parent_id = db.Column(db.BigInteger)
    order_num = db.Column(db.BigInteger)
    path = db.Column(db.String(200))
    component = db.Column(db.String(255))
    query_param = db.Column(db.String(255))
    is_frame = db.Column(db.BigInteger)
    is_cache = db.Column(db.BigInteger)
    menu_type = db.Column(db.String(50))
    visible = db.Column(db.String(50))
    status = db.Column(db.String(50))
    perms = db.Column(db.String(100))
    icon = db.Column(db.String(100))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysNotice(db.Model):
    __tablename__ = 'sys_notice'

    notice_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    notice_title = db.Column(db.String(50))
    notice_type = db.Column(db.String(20))
    notice_content = db.Column(db.String(200))
    status = db.Column(db.String(255))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysOperLog(db.Model):
    __tablename__ = 'sys_oper_log'

    oper_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    title = db.Column(db.String(50))
    business_type = db.Column(db.BigInteger)
    method = db.Column(db.String(100))
    request_method = db.Column(db.String(10))
    operator_type = db.Column(db.BigInteger)
    oper_name = db.Column(db.String(50))
    dept_name = db.Column(db.String(50))
    oper_url = db.Column(db.String(255))
    oper_ip = db.Column(db.String(128))
    oper_location = db.Column(db.String(255))
    oper_param = db.Column(db.String(2000))
    json_result = db.Column(db.String(2000))
    status = db.Column(db.BigInteger)
    error_msg = db.Column(db.String(2000))
    oper_time = db.Column(db.String(500))
    cost_time = db.Column(db.BigInteger)

class SysOss(db.Model):
    __tablename__ = 'sys_oss'

    oss_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    file_name = db.Column(db.String(255))
    original_name = db.Column(db.String(255))
    file_suffix = db.Column(db.String(10))
    url = db.Column(db.String(500))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    service = db.Column(db.String(500))

class SysOssConfig(db.Model):
    __tablename__ = 'sys_oss_config'

    oss_config_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    config_key = db.Column(db.String(20))
    access_key = db.Column(db.String(255))
    secret_key = db.Column(db.String(255))
    bucket_name = db.Column(db.String(255))
    prefix = db.Column(db.String(255))
    endpoint = db.Column(db.String(255))
    domain = db.Column(db.String(255))
    is_https = db.Column(db.String(20))
    region = db.Column(db.String(255))
    access_policy = db.Column(db.String(20))
    status = db.Column(db.String(20))
    ext1 = db.Column(db.String(255))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysPost(db.Model):
    __tablename__ = 'sys_post'

    post_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    post_code = db.Column(db.String(64))
    post_name = db.Column(db.String(50))
    post_sort = db.Column(db.BigInteger)
    status = db.Column(db.String(20))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysRole(db.Model):
    __tablename__ = 'sys_role'

    role_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    role_name = db.Column(db.String(30))
    role_key = db.Column(db.String(100))
    role_sort = db.Column(db.BigInteger)
    data_scope = db.Column(db.String(20))
    menu_check_strictly = db.Column(db.Boolean)
    dept_check_strictly = db.Column(db.Boolean)
    status = db.Column(db.String(20))
    del_flag = db.Column(db.String(20))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))

class SysRoleDept(db.Model):
    __tablename__ = 'sys_role_dept'

    id = db.Column(db.BigInteger, primary_key=True)
    role_id = db.Column(db.BigInteger)
    dept_id = db.Column(db.BigInteger)

class SysRoleMenu(db.Model):
    __tablename__ = 'sys_role_menu'

    id = db.Column(db.BigInteger, primary_key=True)
    role_id = db.Column(db.BigInteger)
    menu_id = db.Column(db.BigInteger)

class SysSocial(db.Model):
    __tablename__ = 'sys_social'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    tenant_id = db.Column(db.String(20))
    auth_id = db.Column(db.String(255))
    source = db.Column(db.String(255))
    open_id = db.Column(db.String(255))
    user_name = db.Column(db.String(30))
    nick_name = db.Column(db.String(20))
    email = db.Column(db.String(255))
    avatar = db.Column(db.String(500))
    access_token = db.Column(db.String(255))
    expire_in = db.Column(db.BigInteger)
    refresh_token = db.Column(db.String(255))
    access_code = db.Column(db.String(255))
    union_id = db.Column(db.String(255))
    scope = db.Column(db.String(255))
    token_type = db.Column(db.String(255))
    id_token = db.Column(db.String(255))
    mac_algorithm = db.Column(db.String(255))
    mac_key = db.Column(db.String(255))
    code = db.Column(db.String(255))
    oauth_token = db.Column(db.String(255))
    oauth_token_secret = db.Column(db.String(255))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    del_flag = db.Column(db.String(20))

class SysTenant(db.Model):
    __tablename__ = 'sys_tenant'

    id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    contact_user_name = db.Column(db.String(20))
    contact_phone = db.Column(db.String(20))
    company_name = db.Column(db.String(50))
    license_number = db.Column(db.String(30))
    address = db.Column(db.String(200))
    intro = db.Column(db.String(200))
    domain = db.Column(db.String(200))
    remark = db.Column(db.String(200))
    package_id = db.Column(db.BigInteger)
    expire_time = db.Column(db.String(200))
    account_count = db.Column(db.BigInteger)
    status = db.Column(db.String(20))
    del_flag = db.Column(db.String(20))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))

class SysTenantPackage(db.Model):
    __tablename__ = 'sys_tenant_package'

    package_id = db.Column(db.BigInteger, primary_key=True)
    package_name = db.Column(db.String(20))
    menu_ids = db.Column(db.String(3000))
    remark = db.Column(db.String(200))
    menu_check_strictly = db.Column(db.BigInteger)
    status = db.Column(db.String(20))
    del_flag = db.Column(db.String(20))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))

class SysUser(db.Model):
    __tablename__ = 'sys_user'

    user_id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.String(20))
    dept_id = db.Column(db.BigInteger)
    user_name = db.Column(db.String(30))
    nick_name = db.Column(db.String(30))
    user_type = db.Column(db.String(10))
    email = db.Column(db.String(50))
    phonenumber = db.Column(db.String(11))
    sex = db.Column(db.String(20))
    avatar = db.Column(db.BigInteger)
    password = db.Column(db.String(100))
    status = db.Column(db.String(20))
    del_flag = db.Column(db.String(20),default='0')
    login_ip = db.Column(db.String(128))
    login_date = db.Column(db.String(255))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))
    remark = db.Column(db.String(500))
    reset_pwd = db.Column(db.Boolean)

class SysUserPost(db.Model):
    __tablename__ = 'sys_user_post'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    post_id = db.Column(db.BigInteger)

class SysUserRole(db.Model):
    __tablename__ = 'sys_user_role'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger)
    role_id = db.Column(db.BigInteger)

class UndoLog(db.Model):
    __tablename__ = 'undo_log'

    branch_id = db.Column(db.BigInteger, primary_key=True)
    xid = db.Column(db.String(100))
    context = db.Column(db.String(128))
    rollback_info = db.Column(db.String(500))
    log_status = db.Column(db.BigInteger)
    log_created = db.Column(db.String(500))
    log_modified = db.Column(db.String(500))

class DataDirectoryAudit(db.Model):
    __tablename__ = 'biz_data_directory_audit'

    id = db.Column(db.BigInteger, primary_key=True)
    data_directory_id = db.Column(db.BigInteger)
    operator_id = db.Column(db.BigInteger)
    operator_name = db.Column(db.String(255))
    operator_time = db.Column(db.String(255))
    audit_result = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    type = db.Column(db.BigInteger)


class DataDirectoryShip(db.Model):
    __tablename__ = 'biz_data_directory_ship'

    id = db.Column(db.BigInteger, primary_key=True)
    data_directory_id = db.Column(db.BigInteger)
    ship_id = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255))
    update_time = db.Column(db.String(255))
    create_id = db.Column(db.BigInteger)

class DataType(db.Model):
    __tablename__ = 'biz_data_type'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255))
    code = db.Column(db.String(255))
    sort_index = db.Column(db.BigInteger)
    type = db.Column(db.BigInteger)

class GenTable(db.Model):
    __tablename__ = 'gen_table'

    table_id = db.Column(db.BigInteger, primary_key=True)
    data_name = db.Column(db.String(255))
    table_name = db.Column(db.String(255))
    table_comment = db.Column(db.String(500))
    sub_table_name = db.Column(db.String(64))
    sub_table_fk_name = db.Column(db.String(64))
    class_name = db.Column(db.String(100))
    tpl_category = db.Column(db.String(200))
    package_name = db.Column(db.String(100))
    module_name = db.Column(db.String(30))
    business_name = db.Column(db.String(30))
    function_name = db.Column(db.String(50))
    function_author = db.Column(db.String(50))
    gen_type = db.Column(db.String(255))
    gen_path = db.Column(db.String(255))
    options = db.Column(db.String(1000))
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(255))
    remark = db.Column(db.String(500))

class GenTableColumn(db.Model):
    __tablename__ = 'gen_table_column'

    column_id = db.Column(db.BigInteger, primary_key=True)
    table_id = db.Column(db.BigInteger)
    column_name = db.Column(db.String(255))
    column_comment = db.Column(db.String(500))
    column_type = db.Column(db.String(100))
    java_type = db.Column(db.String(500))
    java_field = db.Column(db.String(200))
    is_pk = db.Column(db.String(100))
    is_increment = db.Column(db.String(200))
    is_required = db.Column(db.String(100))
    is_insert = db.Column(db.String(30))
    is_edit = db.Column(db.String(30))
    is_list = db.Column(db.String(50))
    is_query = db.Column(db.String(50))
    query_type = db.Column(db.String(255))
    html_type = db.Column(db.String(255))
    dict_type = db.Column(db.String(255))
    sort = db.Column(db.BigInteger)
    create_dept = db.Column(db.BigInteger)
    create_by = db.Column(db.BigInteger)
    create_time = db.Column(db.String(500))
    update_by = db.Column(db.BigInteger)
    update_time = db.Column(db.String(500))

class ServiceObject(db.Model):
    __tablename__ = 'biz_service_object'

    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    code = db.Column(db.String(255))
    create_id = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255))
    update_time = db.Column(db.String(255))
    sort_index = db.Column(db.BigInteger)
    update_id = db.Column(db.BigInteger)

class DataDirectoryFieldShip(db.Model):
    __tablename__ = 'biz_data_directory_field_ship'

    id = db.Column(db.BigInteger, primary_key=True,autoincrement=True)
    data_directory_id = db.Column(db.BigInteger)
    field_id  = db.Column(db.BigInteger)
    ship_data_directory_id = db.Column(db.BigInteger)
    field_name = db.Column(db.String(255))

class DeptBatch(db.Model):
    __tablename__ = 'biz_dept_batch'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    batch_name = db.Column(db.String(255))
    batch_enable = db.Column(db.Boolean)
    create_id = db.Column(db.BigInteger)
    create_time = db.Column(db.String(255))
    create_name = db.Column(db.String(255))