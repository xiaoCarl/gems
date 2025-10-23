"""
最简WebSocket服务器
为聊天界面提供WebSocket接口，直接连接Agent
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 加载环境变量
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from gems.agent import Agent
from gems.logging import get_logger

# 创建日志记录器
logger = get_logger("web_server")

# 创建FastAPI应用
app = FastAPI(title="Gems Chat Server", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局智能体实例
agent = Agent()

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket连接已建立")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket连接已断开")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as send_error:
            logger.error(f"发送消息失败: {send_error}")
            self.disconnect(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except Exception as broadcast_error:
                logger.error(f"广播消息失败: {broadcast_error}")
                self.disconnect(connection)

manager = ConnectionManager()

@app.get("/")
async def get_chat_interface():
    """提供聊天界面"""
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点"""
    await manager.connect(websocket)
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
                
                # 直接调用Agent进行分析（同步方式）
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
    return {"status": "healthy", "connections": len(manager.active_connections)}

if __name__ == "__main__":
    import uvicorn
    
    # 确保在web目录下运行
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    logger.info("启动Gems聊天服务器...")
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )