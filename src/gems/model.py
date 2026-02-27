"""
LLM模型配置
"""

import os
from typing import Any, Type

from gems.config import config


def call_llm(prompt: str, system_prompt: str | None = None, 
             output_schema: Type | None = None, tools: list | None = None) -> Any:
    """
    调用LLM
    
    Args:
        prompt: 用户提示词
        system_prompt: 系统提示词
        output_schema: 输出结构（Pydantic模型）
        tools: 工具列表
    
    Returns:
        LLM响应
    """
    if config.use_qwen and config.dashscope_api_key:
        return _call_qwen(prompt, system_prompt, output_schema, tools)
    elif config.deepseek_api_key:
        return _call_deepseek(prompt, system_prompt, output_schema, tools)
    else:
        raise ValueError("未配置API密钥，请设置 DEEPSEEK_API_KEY 或 DASHSCOPE_API_KEY")


def _call_deepseek(prompt: str, system_prompt: str | None = None,
                   output_schema: Type | None = None, tools: list | None = None) -> Any:
    """调用DeepSeek API"""
    try:
        from langchain_deepseek import ChatDeepSeek
        
        model = ChatDeepSeek(
            model="deepseek-chat",
            api_key=config.deepseek_api_key,
            temperature=0.1,
        )
        
        if output_schema:
            model = model.with_structured_output(output_schema)
        
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))
        
        response = model.invoke(messages)
        return response
        
    except Exception as e:
        raise RuntimeError(f"DeepSeek API调用失败: {e}")


def _call_qwen(prompt: str, system_prompt: str | None = None,
               output_schema: Type | None = None, tools: list | None = None) -> Any:
    """调用Qwen API"""
    try:
        from langchain_qwq import ChatQwen
        
        model = ChatQwen(
            model="qwen-turbo",
            api_key=config.dashscope_api_key,
            temperature=0.1,
        )
        
        if output_schema:
            model = model.with_structured_output(output_schema)
        
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))
        
        response = model.invoke(messages)
        return response
        
    except Exception as e:
        raise RuntimeError(f"Qwen API调用失败: {e}")
