#!/usr/bin/env python3
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from utils.db_pool import DbConnectionPool
from utils.db_client import DbClient
import os

mcp = FastMCP("mysql")

allow_mcp_ddl = os.getenv("ALLOW_MCP_DDL", "false").lower() == "true"

# 数据库配置
db_config = {
    "host": os.getenv("BQM_MYSQL_HOST", "localhost"),
    "port": 3306,
    "user": "bqm",
    "password": os.getenv("BQM_MYSQL_PWD"),
    "database": "bqm"
}
db_pool = DbConnectionPool(db_config)
db_client = DbClient(db_pool)




@mcp.tool()
async def list_databases(random_string: str) -> List[str]:
    """List all accessible databases on the MySQL server"""
    results = db_client.query("SHOW DATABASES")
    return [row['Database'] for row in results]

@mcp.tool()
async def list_tables(database: Optional[str] = None) -> List[str]:
    """List all tables in a specified database"""
    if database:
        db_client.execute(f"USE {database}")
    results = db_client.query("SHOW TABLES")
    return [row[f"Tables_in_{database or db_config['database']}"] for row in results]

@mcp.tool()
async def describe_table(table: str, database: Optional[str] = None) -> List[Dict[str, str]]:
    """Show the schema for a specific table"""
    if database:
        db_client.execute(f"USE {database}")
    results = db_client.query(f"DESCRIBE {table}")
    return [
        {
            "Field": row["Field"],
            "Type": row["Type"],
            "Null": row["Null"],
            "Key": row["Key"],
            "Default": row["Default"],
            "Extra": row["Extra"]
        }
        for row in results
    ]

@mcp.tool()
async def execute_query(query: str, database: Optional[str] = None, allow_mcp_ddl: bool = False) -> List[Dict[str, Any]]:
    """Execute a SQL query. If allow_mcp_ddl is True, DDL operations are allowed."""
    # Check if the query is allowed
    query = query.strip()
    query_lower = query.lower()
    
    # DDL operations check
    ddl_keywords = ['create', 'alter', 'drop', 'truncate', 'rename']
    is_ddl = any(query_lower.startswith(keyword) for keyword in ddl_keywords)
    
    if is_ddl and not allow_mcp_ddl:
        raise ValueError("DDL operations are not allowed. Set allow_mcp_ddl=True to enable DDL operations.")
    
    # For non-DDL operations, only allow read-only queries
    if not is_ddl and not (
        query_lower.startswith('select') or 
        query_lower.startswith('show') or 
        query_lower.startswith('describe') or 
        query_lower.startswith('explain')
    ):
        raise ValueError("Only SELECT, SHOW, DESCRIBE, and EXPLAIN statements are allowed for non-DDL operations")

    if database:
        db_client.execute(f"USE {database}")
        
    # Set a statement timeout for non-DDL queries
    if not is_ddl:
        db_client.execute("SET SESSION MAX_EXECUTION_TIME=5000")  # 5 seconds timeout
    
    # Execute the query
    if is_ddl:
        # For DDL operations, use execute and return affected rows
        affected_rows = db_client.execute(query)
        return [{"affected_rows": affected_rows}]
    else:
        # For read operations, use query and return results
        results = db_client.query(query)
        
        # Convert any non-serializable types to strings
        for row in results:
            for key, value in row.items():
                if isinstance(value, (bytes, bytearray)):
                    row[key] = value.hex()
                elif hasattr(value, 'isoformat'):  # For datetime objects
                    row[key] = value.isoformat()
        
        return results




if __name__ == "__main__":
    mcp.run() 