# coding=utf-8
import random
import os
from datetime import datetime
import requests
import io

from celery import Celery
from kombu.common import PREFETCH_COUNT_MAX
from reportlab.lib.utils import ImageReader

from backend.config import config
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager

matplotlib.use('Agg')
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, \
    PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable
from backend.template.v1_template import REPORT_TITLE_TEMPLATE, REPORT_LABEL_TEMPLATE, REPORT_TOTAL_TEMPLATE, \
    REPORT_LABEL2_TEMPLATE, REPORT_TEXT1_TEMPLATE, REPORT_TEXT2_TEMPLATE, REPORT_TITLE2_TEMPLATE, \
    REPORT_TITLE3_TEMPLATE, NORMATIVE_TITLE_TEMPLATE, NORMATIVE_TEXT_TEMPLATE

if config.get('redis').get('is_password') == False:
    redis_url = f'redis://@{config.get("redis").get("host")}:{config.get("redis").get("port")}'
else:
    redis_url = f'redis://:{config.get("redis").get("password")}@{config.get("redis").get("host")}:{config.get("redis").get("port")}'

current_file_path = os.path.dirname(os.path.abspath(__file__))

class CeleryService:
    app = Celery('distributed_task_demo', broker=f'{redis_url}/0')

    @classmethod
    def send_empty_value_detection_task(
            cls,
            execute_id,
            database_id,
            rule_id,
            table_name,
            field_name
    ):
        """
        封装空值检测任务发送逻辑
        :param execute_id:
        :param database_id:
        :param rule_id:
        :param table_name:
        :param field_name:
        :return:
        """
        return cls.app.send_task("tasks.empty_value_detection",
                                 args=(execute_id, database_id, rule_id, table_name, field_name))

    @classmethod
    def send_repetitive_detection_task(
            cls,
            execute_id,
            database_id,
            rule_id,
            table_name,
            field_name
    ):
        """
        封装质量检测任务发送逻辑
        :param execute_id:
        :param database_id:
        :param rule_id:
        :param table_name:
        :param field_name:
        :return:
        """
        return cls.app.send_task("tasks.repetitive_detection",
                                 args=(execute_id, database_id, rule_id, table_name, field_name))

    @classmethod
    def send_timeliness_detection_task(
            cls,
            database_id,
            table_id
    ):
        """
        封装时效性检测任务发送逻辑
        :param execute_id:
        :param database_id:
        :param rule_id:
        :param table_name:
        :return:
        """

        return cls.app.send_task("tasks.create_timeliness_task", args=(database_id, table_id))

    @classmethod
    def send_generate_report(
            cls,
            database_id,
            table_name,
            execute_id
    ):
        """
        封装生成报告任务发送逻辑
        :param database_id:
        :param table_name:
        :param execute_id:
        :return:
        """
        return cls.app.send_task("tasks.celery_generate_report", args=(database_id, table_name, execute_id))

    @classmethod
    def send_create_task(
            cls,
            database_id,
            table_id
    ):
        """
        封装生成报告任务发送逻辑
        :param database_id:
        :param table_name:
        :param execute_id:
        :return:
        """
        return cls.app.send_task("tasks.create_task", args=(database_id, table_id))

    @classmethod
    def send_create_normative_task(
            cls,
            database_id:list
    ):
        """
        封装生成报告任务发送逻辑
        :param database_id:
        :param table_name:
        :param execute_id:
        :return:
        """
        print(f'-----------------send--{database_id}-----------')
        return cls.app.send_task("tasks.create_normative_task", args=([database_id]))



class HorizontalLine(Flowable):
    def __init__(self, width, height=0.5):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.line(0, self.height / 2, self.width, self.height / 2)


class ReportGenerateService:
    def __init__(self):
        # 注册字体
        pdfmetrics.registerFont(TTFont('SimSun', os.path.dirname(current_file_path) + '/font/FeiHuaSongTi-2.ttf'))
        pdfmetrics.registerFont(TTFont('AozoraMincho-bold', os.path.dirname(current_file_path) + '/font/JiYingHuiPianHuiSong-2.ttf'))
        pdfmetrics.registerFont(TTFont('FangZhengShuSongJianTi-1', os.path.dirname(current_file_path) + '/font/FangZhengShuSongJianTi-1.ttf'))
        font_path = os.path.dirname(current_file_path) + '/font/FeiHuaSongTi-2.ttf'
        fontManager.addfont(font_path)  # 注册字体
        font_prop = FontProperties(fname=font_path)

        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 现在可以用了
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]

        self.styles = getSampleStyleSheet()

    # 定义文档模板
    def go(self, canvas, doc):
        if doc.page == 1:  # 检查是否为第一页
            canvas.saveState()
            canvas.setFillGray(0.9)  # 设置灰色背景，您可以根据需要调整灰度的深浅
            # canvas.rect(0, 0, doc.width, doc.height, fill=True, stroke=False)
            canvas.rect(0, 0, doc.width + 150, doc.height + 150, fill=1)
            canvas.restoreState()
            canvas.setFont('SimSun', 40)
            canvas.drawString(180, 600,
                              "数据质量报告")
            canvas.setFont('SimSun', 20)
            canvas.drawString(190, 350,
                              "检测单位: 广元市数据局")
            canvas.drawString(200, 300,
                              f"检测日期: {datetime.now().strftime('%Y-%m-%d')}")
        else:
            canvas.setFont('AozoraMincho-bold', 10)

            canvas.drawString(100, 810,
                              "本 次 仅 按 照 国 家 和 我 市 已 公 布 的 有 关 数 据 标 准 规 范 质 检 ， 仅 作 参 考")
            canvas.line(doc.leftMargin + 10, 805, doc.width + 75, 805)

    def get_token(self):
        base_url = config.get('llm_url') + '/basic/openapi/auth/v1/api-key/token'
        payload = {
            'ak':config.get('access_key'),
            'sk':config.get('api_key')
        }
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(
                base_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
        except:
            return ''
        return response.json().get('data').get('token')

    def curl_llm_result(self,text):
        token = self.get_token()
        base_url = config.get('llm_url') + '/basic/openapi/engine/chat/v1/completions'
        payload = {
            'appId': config.get('app_id'),
            'messages':[
                {
                    'content':text,
                    'role':'user'
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'token':token
        }
        try:
            # raise '123'
            response = requests.post(
                base_url,
                json=payload,
                headers=headers,
                timeout=1
            )
            response.raise_for_status()
        except:
            return []
        return response.json().get('choices')[0].get('message').get('structOutput').get('result')

    def create_report_code(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y%m%d')
        code = random.randint(10**12,10**13 -1)
        report_code = formatted_date + str(code)
        return report_code

    def create_style(self,
                     name='Normal',
                     parent='Normal',
                     fontSize=0,
                     leading=0,
                     alignment=0,
                     spaceAfter=0,
                     fontName='FangZhengShuSongJianTi-1',
                     spaceBefore=0,
                     firstLineIndent=0
                     ):
        style = ParagraphStyle(
            name,
            parent=self.styles[parent],
            fontSize=fontSize,
            leading=leading,
            alignment=alignment,
            spaceAfter=spaceAfter,
            fontName=fontName,
            spaceBefore=spaceBefore,
            firstLineIndent=firstLineIndent
        )
        return style

    def create_table(self,
                     doc,
                     title_data,
                     data,
                     fontName='FangZhengShuSongJianTi-1',
                     header_background_color=colors.Color(64/255,149/255,229/255,1),
                     header_text_color=colors.whitesmoke,
                     table_background_color=colors.Color(147/255,210/255,243/255,1),
                     table_border_color=colors.black,
                     merge_cells=None
                     ):
        # 获取样本样式
        styles = getSampleStyleSheet()
        # 创建一个样式，用于表格中的文本
        table_style = styles['BodyText']
        table_style.alignment = 1  # 居中
        table_style.fontSize = 10  # 字体大小
        table_style.fontName = fontName  # 字体
        table_data = []
        if title_data != []:
            table_data.append([Paragraph(_item, table_style) for _item in title_data])
        for item in data:
            table_data.append([Paragraph(cell, table_style) for cell in item])
        table = Table(table_data)
        table.splitByRow = True
        # 调整列宽
        col_widths = [doc.width / len(table_data[0]) for _ in range(len(table_data[0]))]
        table._argW = col_widths
        # 调整行高
        for row in table_data:
            max_height = max(cell.wrap(col_widths[table_data.index(row) % len(col_widths)],1000)[1] for cell in row)
            table._argH[table_data.index(row)] = max_height * 2
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), header_background_color),  # 表头背景色
            ('TEXTCOLOR', (0, 0), (-1, 0), header_text_color),  # 表头文字颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 文字居中
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 文字居中
            ('FONTNAME', (0, 0), (-1, 0), fontName),  # 表头字体
            ('FONTSIZE', (0, 0), (-1, 0), 14),  # 表头字体
            # ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 表头底部填充
            ('BACKGROUND', (0, 1), (-1, -1), table_background_color),  # 表格背景色
            ('GRID', (0, 0), (-1, -1), 1, table_border_color),  # 表格边框
            ('FONTNAME', (0, 0), (-1, -1), fontName),  # 内容行字体
            ('FONTSIZE', (0, 0), (-1, -1), 14),  # 内容行字体大小
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 内容行文字居中
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 内容行文字居中
        ]
        if merge_cells:
            for merge in merge_cells:
                style_commands.append(
                    ('SPAN', merge['start'], merge['end'])
                )

        # 添加表格样式
        table.setStyle(TableStyle(style_commands))

        # 合并第一列的前两行

        return table

    def create_plot(self,values,total):
        # 数据
        categories = ['完整性', '一致性', '准确性', '唯一性']
        values = values

        # 正方形的角度（45度、135度、225度、315度）
        angles = [np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4]
        angles += angles[:1]  # 闭合图形

        # 数据也需闭合
        values += values[:1]

        # 创建图形
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

        # 绘制雷达图
        ax.fill(angles, values, color='#1f77b4', alpha=0.25)  # 填充区域
        ax.plot(angles, values, color='#1f77b4', linewidth=2)  # 边界线

        # 设置角度标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        # 在每个维度上显示得分
        for angle, value, label in zip(angles[:-1], values, categories):
            ax.text(angle, value + 5, f'{value}', ha='center', va='center', fontsize=12, color='black')

        # 设置y轴范围和刻度
        ax.set_ylim(0, 30)
        ax.set_yticks(np.arange(0, 120, 10))  # 从0到100，每10为一个刻度
        # 隐藏径向刻度
        ax.set_yticklabels([])

        # 添加网格线
        ax.grid(True, linestyle='--', alpha=0.7)

        # 更改外圈圆圈颜色
        ax.spines['polar'].set_color('white')  # 设置外圈圆圈颜色为红色
        # 设置轴比例，使得雷达图外部为正方形
        ax.set_aspect('equal', 'box')

        # 添加标题
        plt.title('质量评估图', size=15, y=1.05)

        # 显示图例
        plt.legend([f'质量总分{total}'], loc='upper right', bbox_to_anchor=(1.3, 1.1))

        plt.tight_layout()
        return plt

    def get_merge_cells(self, data,length,last=True):

        merge_cells = []
        end_index = 0
        if data.get('integrity') > 0:
            integrity_index = end_index + data.get('integrity')
            merge_cells.append({'start': (0, end_index+1), 'end': (0, integrity_index)})
            if last:
                merge_cells.append({'start': (length, end_index+1), 'end': (length, integrity_index)})
            end_index = integrity_index
        if data.get('consistency') > 0:
            consistency_index = end_index + data.get('consistency')
            merge_cells.append({'start': (0, end_index+1), 'end': (0, consistency_index)})
            if last:
                merge_cells.append({'start': (length, end_index+1), 'end': (length, consistency_index)})
            end_index = consistency_index
        if data.get('accuracy') > 0:
            accuracy_index = end_index + data.get('accuracy')
            merge_cells.append({'start': (0, end_index+1), 'end': (0, accuracy_index)})
            if last:
                merge_cells.append({'start': (length, end_index+1), 'end': (length, accuracy_index)})
            end_index = accuracy_index
        if data.get('repeatability') > 0:
            repeatability_index = end_index + data.get('repeatability')
            merge_cells.append({'start': (0, end_index+1), 'end': (0, repeatability_index)})
            if last:
                merge_cells.append({'start': (length, end_index+1), 'end': (length, repeatability_index)})
        return merge_cells

    def create_pdf(self,
                   file_name: str,
                   dept_name: str,
                   ip: str,
                   database_name: str,
                   report_code: str,
                   check_date: str,
                   check_status: str,
                   check_total: float,
                   data_total: int,
                   table_count: int,
                   field_count: int,
                   success_rule_count:int,
                   rule_total: int,
                   field_table_data2:list,
                   field_table_data: dict,
                   field_table_data3:dict,
                   problem_details: list,
                   normative_data: list,
                   timeless_data: list,
                   normative_status : str = '未检测',
                   timeless_status : str = '未检测'
                   ):
        """
        生成报告
        :param file_name: 文件名
        :param dept_name: 部门名称
        :param ip: 数据库ip地址
        :param database_name: 数据库名称
        :param report_code: 报告编码
        :param check_date: 检测日期
        :param check_status: 检测状态
        :param check_total: 检测得分
        :param data_total: 数据总量
        :param table_count: 表数量
        :param field_count: 数据项数量
        :param rule_total: 规则数量
        :param field_table_data2: 数据质量检测得分统计（质量维度）
        :param field_table_data: 数据质量检测得分统计
        :param field_table_data3: 质量检测依据
        :param problem_details 问题细项
        :param normative_data 规范性检查
        :param normative_status 规范性检测结果
        :param timeless_status 及时性检测结果
        :return:
        """
        file_name = config.get('report_file') + file_name
        doc = BaseDocTemplate(file_name, pagesize=A4)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        template = PageTemplate(id='Normal', frames=[frame], onPage=self.go)
        doc.addPageTemplates([template])

        title_style = self.create_style(name='title', parent='Heading1', fontSize=22, leading=28, alignment=1,
                                        spaceAfter=12, fontName='FangZhengShuSongJianTi-1')
        report_total_style = self.create_style(name='total', parent='Normal', fontSize=14, leading=22, spaceAfter=12)
        report_label_style = self.create_style(name='label', parent='Normal', fontSize=14, leading=22, spaceAfter=12,
                                               fontName='AozoraMincho-bold')
        text_style = self.create_style(name='text', parent='Normal', fontSize=15, leading=30, spaceBefore=20,
                                       spaceAfter=20, firstLineIndent=30)

        title_text = REPORT_TITLE_TEMPLATE.format(database_name=database_name)
        nbsp1 = 21 * '&nbsp;'
        nbsp2 = 55 * '&nbsp;'
        if check_status == '不合格':
            nbsp2 = 51 * '&nbsp;'
        nbsp3 = 39 * '&nbsp;'
        nbsp4 = (55 - len(str(field_count)) * 2) * '&nbsp;'
        nbsp5 = (63 - len(dept_name) * 4) * '&nbsp;'
        nbsp6 = (45 - (len(ip) - 7) * 2)  * '&nbsp;'
        if data_total > 10000:
            str_data_total = str(round(data_total / 10000, 1)) + '万'
        elif data_total > 100000000:
            str_data_total = str(round(data_total / 100000000, 1)) + '亿'
        else:
            str_data_total = str(data_total)
        report_total_text = REPORT_TOTAL_TEMPLATE.format(report_code=report_code, check_date=check_date,table_count=table_count,field_count=field_count,
                                                         dept_name=dept_name,data_total=str_data_total,check_status=check_status, check_total=check_total,
                                                         ip=ip,normative_status=normative_status, timeless_status=timeless_status,database_name=database_name,
                                                         nbsp1=nbsp1,nbsp2=nbsp2,nbsp3=nbsp3,nbsp4=nbsp4,nbsp5=nbsp5,nbsp6=nbsp6)
        report_label_text = REPORT_LABEL_TEMPLATE
        report_text1_text = REPORT_TEXT1_TEMPLATE.format(dept_name=dept_name, check_date=check_date, database_name=database_name)
        report_text2_text = REPORT_TEXT2_TEMPLATE.format(data_total=data_total, field_count=field_count,table_count=table_count,
                                                         rule_total=rule_total,check_total=check_total,success_rule_count=success_rule_count)
        report_label2_text = REPORT_LABEL2_TEMPLATE
        report_title2_text = REPORT_TITLE2_TEMPLATE
        report_title3_text = REPORT_TITLE3_TEMPLATE

        normative_nbsp = (55 - len(normative_status) * 2) * '&nbsp;'
        normative_title_text = NORMATIVE_TITLE_TEMPLATE.format(database_name=database_name)

        elements = []
        elements.append(PageBreak())
        elements.append(Paragraph(title_text, title_style))
        elements.append(Paragraph(report_total_text, report_total_style))
        # 注：此文档已上区块链
        # elements.append(Paragraph(report_label_text, report_label_style))
        # 添加分割线
        line = HorizontalLine(doc.width)
        elements.append(line)
        elements.append(Paragraph(report_text1_text, text_style))
        elements.append(Paragraph(report_text2_text, text_style))
        elements.append(Paragraph(report_label2_text, text_style))

        # 附件1：质量检测依据：
        title_data3 = ['质量维度','规则分类','规则名称','规则描述','规则依据','规则级别','初始得分']
        merge_cells3 = self.get_merge_cells(field_table_data3,6,False)
        elements.append(Paragraph(report_title2_text, report_label_style))
        # field_table_data3 = [['完整性','数据项唯一性','数据项唯一性','GB/T 36344-2018《信息技术 数据质量评价指标》','是']]
        table3 = self.create_table(doc,title_data3, field_table_data3.get('data'))
        elements.append(table3)
        # for item in field_check_info:
        #     elements.append(Paragraph(item, text_style))
        # 附件2：数据质量检测得分统计

        elements.append(Spacer(2, 12))  # 1x12 磅的空白
        elements.append(Paragraph(report_title3_text, report_label_style))

        title_data = ['质量维度', '规则分类', '规则名称', '规则描述', '规则级别', '分值', '表名', '检核字段',
                      '问题条数', '占比（问题记录数/总计路数）', '得分']
        embeding_dict = {
            'integrity': '完整性',
            'consistency': '一致性',
            'accuracy': '准确性',
            'repeatability': '唯一性'
        }
        for index,i in enumerate(field_table_data.get('data').keys()):
            elements.append(Paragraph(f'{index+1}、{embeding_dict.get(i)}', report_label_style))
            result_data = field_table_data.get('data').get(i)
            if not result_data:
                text = '不涉及'
                elements.append(Paragraph(text, text_style))
                continue
            table = self.create_table(doc, title_data,result_data)
            elements.append(table)
            elements.append(Spacer(4, 12))  # 1x12 磅的空白
            print(result_data)
            total = sum([0 if i[5] == '' else float(i[5]) for i in  result_data])
            total_get = sum([0 if i[10] == '' else float(i[10]) for i in  result_data])
            if i == 'integrity':
                weight_total = field_table_data2[0]
            elif i == 'consistency':
                weight_total = field_table_data2[1]
            elif i == 'accuracy':
                weight_total = field_table_data2[2]
            elif i == 'repeatability':
                weight_total = field_table_data2[3]
            text = f"总分值: {total}，总得分: {round(total_get,2)}，质量维度分值: 25，维度得分: {weight_total} ，得分率: {round(weight_total/25*100,2)}%"
            elements.append(Paragraph(text, report_label_style))
        # 附件3：问题细项：按照表分组的问题

        elements.append(Spacer(2, 12))  # 1x12 磅的空白
        elements.append(Paragraph('附件3：问题细项：按照表分组的问题', report_label_style))
        # title_data1 = ['质量维度', '规则分类', '规则名称', '规则描述', '检核表名', '检核字段名', '存储地址', '不符合要求数量','影响范围', '原因']
        for index, problem_data in enumerate(problem_details):
            table2 = self.create_table(doc, [], problem_data.get('data'),header_background_color=colors.Color(147/255,210/255,243/255,1))
            elements.append(Paragraph(f'{index+1}/{len(problem_details)}. {problem_data.get("name")}问题', report_label_style))
            elements.append(table2)
            elements.append(Spacer(4, 12))  # 1x12 磅的空白

        # 附件4：规范性检查结果
        elements.append(Paragraph(normative_title_text, report_label_style))

        for normative in normative_data:
            normative_text = NORMATIVE_TEXT_TEMPLATE.format(table_name=normative.get('table_name'),is_table_comment=normative.get('is_table_comment'),normative_nbsp=normative_nbsp,
                                                            normative_field_count=normative.get('normative_field_count'),field_no_comment=normative.get('field_no_comment'),is_pk=normative.get('is_pk'))
            elements.append(Paragraph(normative_text, report_total_style))
            title_normative_table = ['表名','字段名称','字段类型','字段注释','是否为主键']
            normative_table_data = normative.get('data')
            normative_table = self.create_table(doc,title_normative_table, normative_table_data)
            elements.append(normative_table)
            elements.append(Spacer(4, 12))  # 1x12 磅的空白
        # 附件4：及时性检查结果
        title_timeless_table = ['表名','及时性检查结果']
        timeless_table_data = timeless_data
        timeless_table = self.create_table(doc,title_timeless_table, timeless_table_data)
        elements.append(Paragraph('附件4：及时性检查结果: ', report_label_style))
        elements.append(timeless_table)
        # str_field_table_data2 = [str(i) for i in field_table_data2]
        clean_data = [0 if x is None else x for x in field_table_data2]
        plot_data = [round(clean_data[0]/25*100,2),round(clean_data[1]/25*100,2),round(clean_data[2]/25*100,2),round(clean_data[3]/25*100,2)]
        _plt = self.create_plot(plot_data,check_total)
        # _plt = self.create_plot([80,80.6,77.53,98.66])
        buf = io.BytesIO()
        _plt.savefig(buf, format='png')
        buf.seek(0)
        image = Image(buf, width=350, height=350)

        elements.append(Spacer(4, 12))  # 1x12 磅的空白
        elements.append(image)
        elements.append(Spacer(4, 12))  # 1x12 磅的空白
        title_data2 = ['质量维度','分值','得分','得分率']
        str_field_table_data2 = [
            ['完整性','25',f'{str(field_table_data2[0]) if field_table_data2[0] != None else "-" }',f'{str(round(field_table_data2[0]/25*100,2)) + "%" if field_table_data2[0] != None else "-" }'],
            ['一致性','25',f'{str(field_table_data2[1]) if field_table_data2[1] != None else "-" }',f'{str(round(field_table_data2[1]/25*100,2)) + "%" if field_table_data2[1] != None else "-"  }'],
            ['准确性','25',f'{str(field_table_data2[2]) if field_table_data2[2] != None else "-" }',f'{str(round(field_table_data2[2]/25*100,2)) + "%" if field_table_data2[2] != None else "-"  }'],
            ['唯一性','25',f'{str(field_table_data2[3]) if field_table_data2[3] != None else "-" }',f'{str(round(field_table_data2[3]/25*100,2)) + "%" if field_table_data2[3] != None else "-"  }'],
        ]
        table2 = self.create_table(doc,title_data2, str_field_table_data2)
        elements.append(table2)
        elements.append(Spacer(4, 12))  # 1x12 磅的空白
        elements.append(Paragraph(f'质量总分: {check_total} ', report_label_style))
        elements.append(Paragraph('说明: 质量总分=（完整性得分率 + 一致性得分率 + 准确性得分率 + 唯一性得分率） / 4', report_label_style))
        elements.append(Paragraph('本次报告不参与检测的质量维度，则不参与质量总分计算', report_label_style))
        # 构建文档
        doc.build(elements)
        _plt.close()
        return 'success'


if __name__ == '__main__':
    data2 = [
        {
            'name': '完整性',
            'data':[
            ['表名','biz_database_change_log'],
            ['存储地址','192.168.20.48'],
            ['字段名','create_time'],
            ['原因',''],
            ['不符合要求数量','12'],
            ['影响范围','']
        ]
        },
        {
            'name': '唯一性',
            'data': [
                ['表名', 'biz_database_change_log'],
                ['存储地址', '192.168.20.48'],
                ['字段名', 'create_time'],
                ['原因', ''],
                ['不符合要求数量', '12'],
                ['影响范围', '']
            ]
        }
    ]
    field_table_data3 = {
                        'integrity': 2,
                        'consistency': 2,
                        'accuracy': 0,
                        'repeatability': 0,
                        "data":[['完整性','空值检测','核心字段空值校验', '核心字段存在空值（包括空白值、空格值、NULL值）', 'GB/T 36344-2018《信息技术 数据质量评价指标》', '中度', '20'],
                         ['完整性', '空值检测', '核心字段空值校验', '核心字段存在空值（包括空白值、空格值、NULL值）',
                          'GB/T 36344-2018《信息技术 数据质量评价指标》', '中度', '20'],
                         ['一致性', '空值检测', '核心字段空值校验', '核心字段存在空值（包括空白值、空格值、NULL值）',
                          'GB/T 36344-2018《信息技术 数据质量评价指标》', '中度', '20'],
                         ['一致性', '空值检测', '核心字段空值校验', '核心字段存在空值（包括空白值、空格值、NULL值）',
                          'GB/T 36344-2018《信息技术 数据质量评价指标》', '中度', '20'],
                         ]}
    normative_data = [{'table_name': 'biz_test', 'is_table_comment': '否', 'normative_field_count': 10, 'is_pk': '否',
                       'data': [['biz_test', 'id', 'bigint', '主键', '是'],
                                ['biz_test', 'name', 'varchar', '名称', '否']]}]
    timeless_data = [['biz_test', '不及时']]
    field_table_data = {
                        'integrity': 2,
                        'consistency': 0,
                        'accuracy': 1,
                        'repeatability': 4,
                        "data":{'integrity': [['完整性', '空值检查', '核心字段检查', '', '', '', '', '123', '123','', '25'],
                        ['完整性', '空值检查', '核心字段检查', '', '', '', '', '123', '123','', '25']],
                        'consistency': [['一致性', '空值检查', '核心字段检查', '', '', '', '', '123', '123','', '25'],
                                        ['一致性', '空值检查', '核心字段检查', '', '', '', '', '123', '123', '', '25'],
                                        ['一致性', '空值检查', '核心字段检查', '', '', '', '', '123', '123', '', '25'],
                                        ['一致性', '空值检查', '核心字段检查', '', '', '', '', '123', '123', '', '25'],
                                        ['一致性', '空值检查', '核心字段检查', '', '', '', '', '123', '123', '', '25']],
                        'accuracy': [['准确性', '空值检查', '核心字段检查', '', '', '', '', '123', '123','', '25'],
                                    ['准确性', '空值检查', '核心字段检查', '', '', '', '', '123', '123','', '25']],
                        'repeatability': [['唯一性', '空值检查', '核心字段检查', '', '', '', '', '123', '123','', '25']]

                        }}
    # CeleryService.send_empty_value_detection_task(1, 4, 1, 'biz_data_directory', 'table_id,system_name')
    # CeleryService.send_repetitive_detection_task(1, 4, 1, 'biz_data_directory', 'table_id,system_name')
    # CeleryService.send_timeliness_detection_task(1, 4, 1, 'biz_data_directory', 'update_time','每周')
    # CeleryService.send_generate_report(81, 'biz_data_directory_ship_desc',1, )
    # CeleryService.send_create_normative_task([81,82])
    # CeleryService.send_timeliness_detection_task(81,None)
    # CeleryService.send_create_task(95, None)
    report_service = ReportGenerateService()
    # print(report_service.create_report_code())
    report_service.create_pdf(
        file_name='195409589316275868.pdf',
        dept_name='数字基础设施服务处',
        database_name='bsp-ser',
        ip='132.1.1.1',
        report_code=202508121059319329615,
        check_date='2024-02-01',
        check_status='不合格',
        check_total=0.0,
        data_total=3333049,
        table_count=10,
        field_count=193245,
        rule_total=5,
        success_rule_count=2,
        field_table_data=field_table_data, field_table_data2=[19.72, 0.0, 0.0, 0.0], field_table_data3=field_table_data3,
        problem_details=data2,
        normative_data=normative_data,
        timeless_data=timeless_data
    )
