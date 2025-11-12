REPORT_TITLE_TEMPLATE = """
关于{database_name}数据库的质量检测报告
"""

REPORT_TOTAL_TEMPLATE = """
    报告编码: {report_code}{nbsp1}检测日期: {check_date}<br/>
    质检结果: {check_status}{nbsp2}质检得分: {check_total}<br/>
    检测单位: 广元市数据局{nbsp3}检测表数量: {table_count}张<br/>
    检测字段项: {field_count}项{nbsp4}检测数据量: {data_total}条<br/>
    所属单位: {dept_name}{nbsp5}及时性检测: {timeless_status}
    数据库ip地址: {ip}{nbsp6}规范性检测: {normative_status}<br/>
    数据库名称: {database_name}<br/>
"""

REPORT_LABEL_TEMPLATE = """
注：此文档已上区块链，您可通过"一体化数字资源管理平台"的“实用工具”中的“上链文件校验”验证真伪。
"""

REPORT_TEXT1_TEMPLATE = """
{dept_name}于{check_date}对广元市"一体化数字资源管理平台"中的{database_name}数据库进行了挂接（或更新），此次操作受数据局委托，严格按照国家及我市已公布的相关数据规范要求，对数据库进行了全面的数据质量检测。
"""

REPORT_TEXT2_TEMPLATE = """
该数据库包含共计{data_total}条记录，涉及{table_count}张表，{field_count}个字段。为确保数据质量，我们依据国家、市级以及数据部门的数据标准规范，精心配置并执行了{rule_total}条数据质量检测规则，执行成功{success_rule_count}条。经过严谨的检测流程，该数据库的数据质检得分为{check_total}分。
"""

REPORT_LABEL2_TEMPLATE = """
具体的问题清单已整理成附表，供数源部门及经审批同意共享的申请部门查阅，以便针对性地进行数据整改和提升。我们将持续关注数据质量，确保数据库的准确性和可靠性，为广元市的数据管理和政务服务提供有力支持。
"""

REPORT_TITLE2_TEMPLATE = """
附件1：质量检测依据:
"""

REPORT_TITLE3_TEMPLATE = """
附件2：数据质量检测得分统计:
"""

NORMATIVE_TITLE_TEMPLATE = """
附件4:  {database_name}数据规范性检测结果:
"""

NORMATIVE_TEXT_TEMPLATE = """
表名: {table_name}<br/>
是否有表注释: {is_table_comment}{normative_nbsp}是否含有主键: {is_pk}<br/>
字段数量: {normative_field_count}{normative_nbsp}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;字段无注释数量: {field_no_comment}
"""

