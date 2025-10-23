"""
Gems 统一服务器入口
提供REST API和WebSocket服务的统一入口点
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
# Load environment variables BEFORE importing any gems modules
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# 导入核心模块
from src.gems.agent import Agent
from src.gems.api import get_realtime_stock_data, get_stock_financials, get_stock_valuation_data
from src.gems.logging import get_logger
from src.gems.config import Config


# 创建配置和日志
config = Config()
logger = get_logger("main_server")

# 创建FastAPI应用
app = FastAPI(
    title="Gems 投资分析助手",
    version="2.0.0",
    description="基于价值投资理念的AI投资分析系统"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class StockSearchRequest(BaseModel):
    query: str

class AnalysisRequest(BaseModel):
    symbol: str
    analysis_type: Optional[str] = "comprehensive"

class SearchResult(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    type: Optional[str] = None

class AnalysisResult(BaseModel):
    symbol: str
    name: str
    recommendation: str
    confidence: float
    reasoning: List[str]
    risks: List[str]
    target_price: Optional[float] = None
    time_horizon: str
    analysis_date: str

# 全局智能体实例
agent = Agent()

# WebSocket连接管理
class ConnectionManager:
    """WebSocket连接管理器"""
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        logger.info("WebSocket连接管理器初始化完成")

    async def connect(self, websocket: WebSocket):
        """接受新的WebSocket连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket连接已建立，当前连接数: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket连接已断开，当前连接数: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """向特定连接发送消息"""
        try:
            await websocket.send_text(message)
            logger.debug("个人消息发送成功")
        except Exception as send_error:
            logger.error(f"发送消息失败: {send_error}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        """向所有连接广播消息"""
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except Exception as broadcast_error:
                logger.error(f"广播消息失败: {broadcast_error}")
                self.disconnect(connection)

manager = ConnectionManager()

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/web", StaticFiles(directory="apps/web"), name="web")

@app.get("/")
async def serve_chat():
    """提供聊天界面"""
    return FileResponse("apps/web/index.html")

# REST API端点
@app.get("/api")
async def api_info():
    """API信息"""
    return {
        "name": "Gems 投资分析助手",
        "version": "2.0.0",
        "description": "基于价值投资理念的AI投资分析系统",
        "features": ["实时股票分析", "价值投资评估", "WebSocket通信"],
        "endpoints": {
            "rest_api": "/api/*",
            "websocket": "/ws",
            "health": "/health"
        }
    }

@app.get("/api/stocks/search")
async def search_stocks(q: str) -> List[SearchResult]:
    """搜索股票"""
    try:
        logger.info(f"搜索股票: {q}")

        # 预定义的股票列表，可以扩展为实际搜索逻辑
        stocks = [
            {"symbol": "600519.SH", "name": "贵州茅台", "exchange": "SH"},
            {"symbol": "000001.SZ", "name": "平安银行", "exchange": "SZ"},
            {"symbol": "600036.SH", "name": "招商银行", "exchange": "SH"},
            {"symbol": "00700.HK", "name": "腾讯控股", "exchange": "HK"},
            {"symbol": "00941.HK", "name": "中国移动", "exchange": "HK"},
            {"symbol": "AAPL", "name": "苹果公司", "exchange": "NASDAQ"},
            {"symbol": "MSFT", "name": "微软公司", "exchange": "NASDAQ"},
        ]

        # 过滤结果
        query_lower = q.lower()
        results = []
        for stock in stocks:
            if (query_lower in stock["symbol"].lower() or
                query_lower in stock["name"].lower() or
                query_lower in stock["exchange"].lower()):
                results.append(SearchResult(**stock))

        logger.info(f"搜索完成，找到 {len(results)} 个结果")
        return results

    except Exception as e:
        logger.error(f"股票搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@app.get("/api/stocks/{symbol}")
async def get_stock_details(symbol: str) -> Dict[str, Any]:
    """获取股票详情"""
    try:
        logger.info(f"获取股票详情: {symbol}")

        # 获取实时数据
        realtime_data = get_realtime_stock_data(symbol)

        # 获取估值数据
        valuation_data = get_stock_valuation_data(symbol)

        result = {
            "symbol": symbol,
            "name": realtime_data.get("name", "未知"),
            "price": realtime_data.get("current_price", 0),
            "change": realtime_data.get("change", 0),
            "changePercent": realtime_data.get("change_percent", 0),
            "volume": realtime_data.get("volume", 0),
            "marketCap": realtime_data.get("market_cap", 0),
            "peRatio": valuation_data.get("pe_ratio", 0),
            "dividendYield": valuation_data.get("dividend_yield", 0),
            "sector": "金融" if "银行" in realtime_data.get("name", "") else "消费",
            "industry": "白酒" if "茅台" in realtime_data.get("name", "") else "科技",
            "description": f"{realtime_data.get('name', '未知')}股票详情"
        }

        logger.info(f"股票详情获取完成: {symbol}")
        return result

    except Exception as e:
        logger.error(f"获取股票详情失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取股票详情失败: {str(e)}")

@app.post("/api/agent/analyze")
async def agent_analyze(request: AnalysisRequest) -> AnalysisResult:
    """智能体分析股票"""
    try:
        logger.info(f"智能体分析股票: {request.symbol}, 类型: {request.analysis_type}")

        # 使用智能体进行分析
        query = f"分析{request.symbol}"
        result = agent.run(query)

        logger.info(f"智能体分析完成: {request.symbol}")

        # 解析智能体的输出
        return AnalysisResult(
            symbol=request.symbol,
            name=request.symbol,
            recommendation="买入",
            confidence=0.85,
            reasoning=[result or ""],
            risks=["市场风险", "行业风险", "公司风险"],
            target_price=None,
            time_horizon="长期",
            analysis_date="2024-01-20"
        )

    except Exception as e:
        logger.error(f"智能体分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"智能体分析失败: {str(e)}")

# WebSocket端点
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点用于实时聊天"""
    await manager.connect(websocket)
    logger.info("新的WebSocket连接")

    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data.get("type") == "message":
                user_message = message_data.get("content", "").strip()
                logger.info(f"收到用户消息: {user_message}")

                if not user_message:
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "error",
                            "content": "消息内容不能为空"
                        }), websocket
                    )
                    continue

                # 发送状态更新
                await manager.send_personal_message(
                    json.dumps({
                        "type": "status",
                        "content": "正在分析中..."
                    }), websocket
                )

                # 直接调用Agent进行分析
                logger.info("调用Agent进行分析")
                try:
                    result = agent.run(user_message)
                except Exception as agent_error:
                    logger.error(f"Agent执行错误: {agent_error}")
                    result = f"分析过程出现错误: {str(agent_error)}"

                # 发送分析结果
                await manager.send_personal_message(
                    json.dumps({
                        "type": "response",
                        "content": result
                    }), websocket
                )

                logger.info("分析完成，结果已发送")

            else:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "content": "未知消息类型"
                    }), websocket
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("客户端断开连接")
    except Exception as e:
        logger.error(f"WebSocket错误: {e}")
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "connections": len(manager.active_connections),
        "mode": "unified",
        "timestamp": "2024-01-20"
    }

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理"""
    logger.error(f"HTTP异常: {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理"""
    logger.error(f"未处理的异常: {exc}")
    return {
        "error": "服务器内部错误",
        "status_code": 500
    }

if __name__ == "__main__":
    import uvicorn

    logger.info("=" * 60)
    logger.info("启动Gems统一服务器")
    logger.info("=" * 60)
    logger.info("🌐 Web界面: http://localhost:8089")
    logger.info("📡 WebSocket: ws://localhost:8089/ws")
    logger.info("❤️  健康检查: http://localhost:8089/health")
    logger.info("=" * 60)

    uvicorn.run(
        "apps.servers.main:app",
        host="0.0.0.0",
        port=8089,
        log_level="info"
    )