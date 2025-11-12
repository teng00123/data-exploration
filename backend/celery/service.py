
class DbService:

    @classmethod
    def create_table(cls, session, model,commit=True, **kwargs):
        """
        通用的表数据插入方法

        :param session: sqlalchemy会话
        :param model: 要插入的模型类
        :param data: 包含字段值的字典
        :param kwargs: 额外的字段值
        :return: 插入的记录对象
        """
        # print(**kwargs)
        record = model(**kwargs)

        session.add(record)
        if commit:
            session.commit()
        else:
            session.flush()
        session.close()
        return record


    @classmethod
    def update_record(cls, session, model, **kwargs):
        """
        通用的表数据更新方法

        :param session: sqlalchemy会话
        :param model: 要更新的模型类
        :param record_id: 要更新的记录ID
        :param kwargs: 要更新的字段和值
        :return: 更新后的记录对象
        """
        for key, value in kwargs.items():
            setattr(model, key, value)

        session.commit()
        session.close()
        return model

    @classmethod
    def query_records(cls, session, model, filters=None, order_by=None, limit=None, filter=None, first=False):
        """
        通用的表数据查询方法

        :param session: sqlalchemy会话
        :param model: 要查询的模型类
        :param filters: 查询条件字典，例如 {'name': 'Alice', 'age': 25}
        :param order_by: 排序条件，例如 'name' 或 '-age'（降序）
        :param limit: 返回记录的最大数量
        :param filter: filter查询条件，例如 DatabaseChangeLog.change_status.in_(['update', 'add', 'delete'])
        :param first: 是否只返回第一条记录
        :return: 查询结果列表
        """
        query = session.query(model)

        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(model, key) == value)

        if filter:
            query = query.filter(filter)

        # 应用排序条件
        if order_by:
            if order_by.startswith('-'):
                column = getattr(model, order_by[1:])
                query = query.order_by(column.desc())
            else:
                query = query.order_by(getattr(model, order_by))

        # 应用限制条件
        if limit:
            query = query.limit(limit)

        if first:
            result = query.first().__dict__ if query.first() else {}
            return {k: v for k, v in  result.items() if k != '_sa_instance_state'}

        return  [{k: v for k, v in i.__dict__.items() if k != '_sa_instance_state'} for i in query.all()]

    @classmethod
    def upsert_record(cls, session, model, unique_filters, update_data, commit=True):
        """
        根据条件查询记录，有则更新无则新增

        :param session: sqlalchemy会话
        :param model: 要操作的模型类
        :param unique_filters: 查询条件的字典，例如 {'name': 'Alice'}
        :param update_data: 要更新的字段和值的字典
        :param commit: 是否提交事务
        :return: 插入或更新后的记录对象
        """
        # 查询记录
        query = session.query(model)
        for key, value in unique_filters.items():
            query = query.filter(getattr(model, key) == value)
        record = query.first()

        if record:
            # 更新记录
            for key, value in update_data.items():
                setattr(record, key, value)
        else:
            new_data = {**unique_filters, **update_data}
            # 插入新记录
            record = model(**new_data)
            session.add(record)

        if commit:
            session.commit()
        else:
            session.flush()
        session.close()
        return record