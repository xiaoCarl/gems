"""
AI Agent 核心模块
"""

import time

from langchain_core.messages import AIMessage

from gems.cache.manager import cache_manager
from gems.logging import get_logger
from gems.model import call_llm
from gems.prompts import (
    ACTION_SYSTEM_PROMPT,
    PLANNING_SYSTEM_PROMPT,
    VALUE_INVESTING_SYSTEM_PROMPT,
)
from gems.schemas import Answer, IsDone, StockConfirmation, TaskList
from gems.tools import TOOLS


class Agent:
    """价值投资分析Agent"""
    
    def __init__(self, max_steps: int = 20, max_steps_per_task: int = 5, use_web_output: bool = False):
        self.max_steps = max_steps
        self.max_steps_per_task = max_steps_per_task
        self.use_web_output = use_web_output
        self.logger = get_logger("agent")
    
    def _confirm_stock_info(self, query: str) -> tuple[bool, StockConfirmation]:
        """确认股票信息"""
        prompt = f"用户查询: {query}\n请确认股票信息。"
        
        try:
            confirmation = call_llm(
                prompt,
                system_prompt="从用户查询中提取股票名称和代码。",
                output_schema=StockConfirmation
            )
            return True, confirmation
        except Exception as e:
            self.logger.error(f"确认股票信息失败: {e}")
            return False, None
    
    def plan_tasks(self, query: str) -> list:
        """规划任务"""
        tool_descriptions = "\n".join([
            f"- {t.name}: {t.description}" for t in TOOLS
        ])
        
        prompt = f"用户查询: {query}\n可用工具：\n{tool_descriptions}"
        
        try:
            response = call_llm(
                prompt,
                system_prompt=PLANNING_SYSTEM_PROMPT,
                output_schema=TaskList
            )
            return response.tasks
        except Exception as e:
            self.logger.error(f"任务规划失败: {e}")
            return []
    
    def ask_for_actions(self, task_desc: str, last_outputs: str = "") -> AIMessage:
        """请求下一步行动"""
        prompt = f"任务: {task_desc}\n历史输出: {last_outputs}\n请决定下一步行动。"
        
        try:
            response = call_llm(
                prompt,
                system_prompt=ACTION_SYSTEM_PROMPT,
                tools=TOOLS
            )
            return response
        except Exception as e:
            self.logger.error(f"请求行动失败: {e}")
            return AIMessage(content="继续分析")
    
    def ask_if_done(self, task_desc: str, recent_results: str) -> bool:
        """询问任务是否完成"""
        prompt = f"任务: {task_desc}\n结果: {recent_results}\n任务是否完成？"
        
        try:
            response = call_llm(
                prompt,
                system_prompt="判断任务是否完成。",
                output_schema=IsDone
            )
            return response.done
        except Exception:
            return False
    
    def _generate_answer(self, query: str, session_outputs: list) -> str:
        """生成最终答案"""
        all_results = "\n\n".join(session_outputs) if session_outputs else "无数据"
        
        prompt = f"""
用户查询: {query}

收集的数据：
{all_results}

请基于以上数据，提供全面的价值投资分析报告。
"""
        
        try:
            response = call_llm(
                prompt,
                system_prompt=VALUE_INVESTING_SYSTEM_PROMPT,
                output_schema=Answer
            )
            return response.answer
        except Exception as e:
            self.logger.error(f"生成答案失败: {e}")
            return f"分析过程中出现错误: {e}"
    
    def run(self, query: str) -> str:
        """
        执行分析
        
        Args:
            query: 用户查询
        
        Returns:
            分析报告
        """
        self.logger.info(f"开始分析: {query}")
        
        # 确认股票信息
        confirmed, confirmation = self._confirm_stock_info(query)
        if not confirmed or not confirmation or not confirmation.stock_code:
            return "无法识别股票信息，请提供有效的股票代码或名称。"
        
        symbol = confirmation.stock_code
        
        # 检查缓存
        cached_result = cache_manager.get_analysis_result(symbol)
        if cached_result:
            self.logger.info(f"使用缓存: {symbol}")
            return f"【缓存结果】\n\n{cached_result}"
        
        # 规划任务
        tasks = self.plan_tasks(query)
        if not tasks:
            tasks = [{"id": 1, "description": query, "done": False}]
        
        # 执行任务
        session_outputs = []
        step_count = 0
        
        for task in tasks:
            if step_count >= self.max_steps:
                break
            
            task_outputs = []
            
            while step_count < self.max_steps:
                # 获取下一步行动
                ai_message = self.ask_for_actions(task.description, "\n".join(task_outputs))
                
                # 检查是否有工具调用
                if not hasattr(ai_message, "tool_calls") or not ai_message.tool_calls:
                    break
                
                # 执行工具调用
                for tool_call in ai_message.tool_calls:
                    tool_name = tool_call.get("name", "")
                    tool_args = tool_call.get("args", {})
                    
                    # 查找并执行工具
                    tool = next((t for t in TOOLS if t.name == tool_name), None)
                    if tool:
                        try:
                            result = tool.invoke(tool_args)
                            output = f"{tool_name}: {result}"
                            session_outputs.append(output)
                            task_outputs.append(output)
                        except Exception as e:
                            error = f"{tool_name} 错误: {e}"
                            session_outputs.append(error)
                            task_outputs.append(error)
                    
                    step_count += 1
                
                # 检查任务是否完成
                if self.ask_if_done(task.description, "\n".join(task_outputs)):
                    break
        
        # 生成最终答案
        answer = self._generate_answer(query, session_outputs)
        
        # 缓存结果
        cache_manager.set_analysis_result(symbol, answer)
        
        return answer
