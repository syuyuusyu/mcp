import httpx
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp_api_getway")

@mcp.tool()
async def api_document(url: str) -> Dict:
    """
    获取API文档
    
    Args:
        url: Swagger文档地址，通常为 /api-docs 或 /swagger.json
    Returns:
        Dict: API文档内容
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to fetch API document: {response.status_code}"}
        return response.json()

@mcp.tool()
async def call_api(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    body: Optional[Any] = None
) -> Dict:
    """
    调用API接口
    
    Args:
        method: HTTP方法 (GET, POST, PUT, DELETE等)
        url: 完整的API URL
        headers: 请求头
        params: 查询参数
        body: 请求体
    Returns:
        Dict: 包含status_code、headers和content的响应
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            json=body if method.upper() not in ["GET", "DELETE"] else None
        )
        
        content = response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": content
        }



if __name__ == "__main__":
    mcp.run()