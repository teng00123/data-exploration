import datetime
from typing import Type, List, Optional, Dict, Any, Union

from sqlalchemy.sql import and_, or_,desc,asc,func
from sqlalchemy.orm import Query
from sqlalchemy import ColumnElement
from backend.config import db
from typing import Type, TypeVar, Optional, List

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True,comment='主键')
    created_at = db.Column(db.DateTime,default=datetime.datetime.utcnow,comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,comment='更新时间')

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

# 定义一个类型变量，用于泛型
T = TypeVar('T', bound='BaseModel')

# 通用CRUD类
class GenericCRUD:
    @staticmethod
    def create(model_class: Type[T], **kwargs) -> T:
        """
        创建并保存一个新记录
        :param model_class: 模型类
        :param kwargs: 模型属性
        :return: 创建的模型实例
        """
        instance = model_class(**kwargs)
        instance.save()
        return instance

    @staticmethod
    def get_by_id(model_class: Type[T], id: int) -> Optional[T]:
        """
        根据ID获取记录
        :param model_class: 模型类
        :param id: 记录ID
        :return: 模型实例或None
        """
        return model_class.query.get(id)

    @staticmethod
    def get_all(model_class: Type[T]) -> List[T]:
        """
        获取所有记录
        :param model_class: 模型类
        :return: 模型实例列表
        """
        return [{ k: v for k, v in  i.__dict__.items() if k != '_sa_instance_state'} for i in model_class.query.all()]

    @staticmethod
    def query_by_conditions(
            model_class: Type[T],
            conditions: Optional[Union[ColumnElement[bool], List[ColumnElement[bool]]]] = None,
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[Union[str, List[str]]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            group_by: Optional[str] = None,
            first = False
    ):
        """
        通用的条件查询方法

        :param model_class: 模型类
        :param conditions: SQLAlchemy条件表达式或条件表达式列表
        :param filters: 关键字参数形式的查询条件
        :param order_by: 排序字段，可以是字符串或字符串列表
        :param limit: 返回记录数限制
        :param offset: 返回记录偏移量
        :param first: 是否只返回第一条记录
        :return: 模型实例列表
        """
        query: Query = model_class.query

        # 处理复杂条件
        if conditions is not None:
            if isinstance(conditions, (list, tuple)):
                query = query.filter(and_(*conditions))
            else:
                query = query.filter(conditions)

        # 处理简单条件
        if filters is not None:
            query = query.filter_by(**filters)
        # 处理分组
        if group_by is not None:
            query = query.group_by(getattr(model_class, group_by))

        # 处理排序
        if order_by is not None:
            if isinstance(order_by, (list, tuple)):
                order_expressions = []
                for field in order_by:
                    if field.startswith('-'):
                        order_expressions.append(getattr(model_class, field[1:]).desc())
                    else:
                        order_expressions.append(getattr(model_class, field).asc())
                query = query.order_by(*order_expressions)
            else:
                if order_by.startswith('-'):
                    query = query.order_by(getattr(model_class, order_by[1:]).desc())
                else:
                    query = query.order_by(getattr(model_class, order_by).asc())

        # 处理分页
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if first:
            result = query.first().__dict__ if query.first() else {}
            return {k: v for k, v in  result.items() if k != '_sa_instance_state'}
        result = query.all() if query.first() else []
        return  [{k: v for k, v in i.__dict__.items() if k != '_sa_instance_state'} for i in result]

    @staticmethod
    def query_by_conditions_group(
            model_class: Type[T],
            conditions: Optional[Union[ColumnElement[bool], List[ColumnElement[bool]]]] = None,
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[Union[str, List[str]]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            group_by: Optional[Union[str, List[str]]] = None,
            aggregate_funcs: Optional[Dict[str, str]] = None,
            first: bool = False
    ):
        """
        通用的条件查询方法，支持分组查询和聚合函数

        :param model_class: 模型类
        :param conditions: SQLAlchemy条件表达式或条件表达式列表
        :param filters: 关键字参数形式的查询条件
        :param order_by: 排序字段，可以是字符串或字符串列表
        :param limit: 返回记录数限制
        :param offset: 返回记录偏移量
        :param group_by: 分组字段，可以是字符串或字符串列表
        :param aggregate_funcs: 聚合函数字典，如 {'count': 'id', 'avg': 'price'}
        :param first: 是否只返回第一条记录
        :return: 模型实例列表
        """
        query = model_class.query

        # 处理复杂条件
        if conditions is not None:
            if isinstance(conditions, (list, tuple)):
                query = query.filter(and_(*conditions))
            else:
                query = query.filter(conditions)

        # 处理简单条件
        if filters is not None:
            query = query.filter_by(**filters)

        # 处理分组和聚合
        if group_by is not None:
            if isinstance(group_by, (list, tuple)):
                group_columns = [getattr(model_class, col) for col in group_by]
            else:
                group_columns = [getattr(model_class, group_by)]

            # 构建select子句
            select_columns = group_columns.copy()

            # 添加聚合函数
            if aggregate_funcs is not None:
                for func_name, column_name in aggregate_funcs.items():
                    if func_name.lower() == 'count':
                        select_columns.append(
                            func.count(getattr(model_class, column_name)).label(f'count_{column_name}'))
                    elif func_name.lower() == 'sum':
                        select_columns.append(func.sum(getattr(model_class, column_name)).label(f'sum_{column_name}'))
                    elif func_name.lower() == 'avg':
                        select_columns.append(func.avg(getattr(model_class, column_name)).label(f'avg_{column_name}'))
                    elif func_name.lower() == 'min':
                        select_columns.append(func.min(getattr(model_class, column_name)).label(f'min_{column_name}'))
                    elif func_name.lower() == 'max':
                        select_columns.append(func.max(getattr(model_class, column_name)).label(f'max_{column_name}'))

            query = query.with_entities(*select_columns).group_by(*group_columns)

        # 处理排序
        if order_by is not None:
            if isinstance(order_by, (list, tuple)):
                order_expressions = []
                for field in order_by:
                    if field.startswith('-'):
                        order_expressions.append(getattr(model_class, field[1:]).desc())
                    else:
                        order_expressions.append(getattr(model_class, field).asc())
                query = query.order_by(*order_expressions)
            else:
                if order_by.startswith('-'):
                    query = query.order_by(getattr(model_class, order_by[1:]).desc())
                else:
                    query = query.order_by(getattr(model_class, order_by).asc())

        # 处理分页
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if query.first():
            if first:
                return query.first()
            return query.all()
        else:
            if first:
                return (None,None)
            return []

    @staticmethod
    def update(model_class: Type[T], id: int, **kwargs) -> Optional[T]:
        """
        更新记录
        :param model_class: 模型类
        :param id: 记录ID
        :param kwargs: 要更新的属性
        :return: 更新后的模型实例或None
        """
        instance = GenericCRUD.get_by_id(model_class, id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
        return instance

    @staticmethod
    def delete(model_class: Type[T], id: int) -> bool:
        """
        删除记录
        :param model_class: 模型类
        :param id: 记录ID
        :return: 是否删除成功
        """
        instance = GenericCRUD.get_by_id(model_class, id)
        if instance:
            instance.delete()
            return True
        return False