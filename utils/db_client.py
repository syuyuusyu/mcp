# app/services/db_client.py
from sqlalchemy.sql import text

class DbClient:
    def __init__(self, pool):
        """
        初始化 DbClient，使用 SQLAlchemy 连接池。

        Args:
            pool (DbConnectionPool): 数据库连接池
        """
        self.engine = pool.get_engine()
        self.connection = None

    def query(self, sql, params=None):
        """
        执行 SQL 查询并返回结果。

        Args:
            sql (str): SQL 查询语句
            params (dict, optional): 查询参数

        Returns:
            list: 查询结果（字典列表）
        """
        try:
            self.connection = self.engine.connect()
            if params:
                result = self.connection.execute(text(sql), params)
            else:
                result = self.connection.execute(text(sql))
            results = [row._asdict() for row in result.fetchall()]
            return results
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None

    def insert(self, sql, params=None):
        """
        执行 INSERT 语句，返回受影响的行数。
        """
        try:
            self.connection = self.engine.connect()
            if params:
                result = self.connection.execute(text(sql), params)
            else:
                result = self.connection.execute(text(sql))
            return result.rowcount
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None

    def update(self, sql, params=None):
        """
        执行 UPDATE 语句，返回受影响的行数。
        """
        try:
            self.connection = self.engine.connect()
            if params:
                result = self.connection.execute(text(sql), params)
            else:
                result = self.connection.execute(text(sql))
            return result.rowcount
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None

    def delete(self, sql, params=None):
        """
        执行 DELETE 语句，返回受影响的行数。
        """
        try:
            self.connection = self.engine.connect()
            if params:
                result = self.connection.execute(text(sql), params)
            else:
                result = self.connection.execute(text(sql))
            return result.rowcount
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None

    def execute(self, sql, params=None):
        """
        执行任意 SQL 语句，返回受影响的行数。
        主要用于执行 DDL 语句或其他不返回结果集的语句。

        Args:
            sql (str): SQL 语句
            params (dict, optional): 查询参数

        Returns:
            int: 受影响的行数
        """
        try:
            self.connection = self.engine.connect()
            if params:
                result = self.connection.execute(text(sql), params)
            else:
                result = self.connection.execute(text(sql))
            return result.rowcount
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            self.connection = None