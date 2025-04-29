from mcp.server.fastmcp import FastMCP
from utils.db_pool import DbConnectionPool
from utils.db_client import DbClient
mcp = FastMCP("prompt_cache")

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "rest"
}
db_pool = DbConnectionPool(db_config)
db_client = DbClient(db_pool)

@mcp.tool()
async def save_prompt_cache(prompt_name: str, prompt_content: str) -> str:
    """
    保存提示词缓存
    
    Args:
        prompt_name: 提示词标题
        prompt_content: 提示词内容
    """
    
    count_result = db_client.query(
        "SELECT COUNT(*) as cnt FROM prompt_cache WHERE name = :name",
        {"name": prompt_name}
    )
    count = count_result[0]['cnt'] if count_result else 0
    if count > 0:
        sql = "UPDATE prompt_cache SET content = :content WHERE name = :name"
    else:
        sql = "INSERT INTO prompt_cache (name, content) VALUES (:name, :content)"
    affected_rows =db_client.insert(
        sql,
        {"name": prompt_name, "content": prompt_content}
    )
    return f"保存成功，影响行数：{affected_rows}"
    
@mcp.tool()
async def get_prompt_cache(prompt_name: str) -> str:
    """
    获取提示词缓存
    """
    return db_client.query(
        "SELECT content FROM prompt_cache WHERE name = :name",
        {"name": prompt_name}
    )

if __name__ == "__main__":
    # 使用默认的 stdio 传输运行服务器
    mcp.run()