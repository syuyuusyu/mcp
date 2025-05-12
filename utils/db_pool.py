# app/services/db_pool.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from urllib.parse import quote_plus

class DbConnectionPool:
    def __init__(self,config):
        """
        初始化 SQLAlchemy 连接池。

        Args:
            config (dict): 数据库配置
        """
        encoded_password = quote_plus(config['password'])
        connection_string = (
            f"mysql+pymysql://{config['user']}:{encoded_password}@"
            f"{config['host']}:{config.get('port', 3306)}/{config['database']}?charset=utf8mb4"
        )
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=2,  # 减少基础连接池大小到2
            max_overflow=1,  # 最多允许1个额外连接
            pool_timeout=30,  # 获取连接超时时间
            pool_pre_ping=True,  # 保持启用连接池心跳检测
            pool_recycle=600,  # 减少连接回收时间到10分钟，保持连接新鲜
            pool_use_lifo=True,  # 保持使用LIFO策略，优先复用最近的连接
            isolation_level='AUTOCOMMIT',
            # 优化连接参数，增加稳定性
            connect_args={
                'connect_timeout': 20,  # 增加连接超时时间，确保能建立连接
                'read_timeout': 60,     # 增加读取超时时间，避免长查询断开
                'write_timeout': 30     # 写入超时保持不变
            }
        )

    def get_engine(self):
        return self.engine

    def close(self):
        self.engine.dispose()