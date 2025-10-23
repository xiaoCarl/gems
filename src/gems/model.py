import os
import time
from typing import Any, cast

from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_deepseek import ChatDeepSeek
from langchain_qwq import ChatQwQ
from pydantic import BaseModel, SecretStr

from gems.logging import get_logger
from gems.prompts import DEFAULT_SYSTEM_PROMPT


# Determine which model to use based on environment variables
def _get_llm():
    """Initialize the appropriate LLM based on environment variables."""
    # Check for QwQ configuration
    if os.getenv("USE_QWEN") == "true":
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY environment variable is required for QwQ"
            )
        return ChatQwQ(
            model="qwen-plus",
            temperature=float(os.getenv("QWQ_TEMPERATURE", "0")),
            api_key=api_key,
        )

    # Default to DeepSeek
    api_key = os.getenv("DEEPSEEK_API_KEY")
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=0,
        api_key=SecretStr(api_key) if api_key else None,
    )


# Initialize the LLM
llm = _get_llm()


def call_llm(
    prompt: str,
    system_prompt: str | None = None,
    output_schema: type[BaseModel] | None = None,
    tools: list[BaseTool] | None = None,
) -> Any:
    logger = get_logger("model")

    final_system_prompt = system_prompt if system_prompt else DEFAULT_SYSTEM_PROMPT

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", final_system_prompt), ("user", "{prompt}")]
    )

    runnable: Runnable = cast(Runnable, llm)
    if output_schema:
        runnable = cast(
            Runnable,
            llm.with_structured_output(output_schema, method="function_calling"),
        )
    elif tools:
        runnable = cast(Runnable, llm.bind_tools(tools))

    chain = prompt_template | runnable

    # Retry logic for transient connection errors
    for attempt in range(3):
        try:
            start_time = time.time()
            logger.debug(
                "LLM调用开始",
                attempt=attempt + 1,
                output_schema=output_schema.__name__ if output_schema else None,
                tools_count=len(tools) if tools else 0,
            )

            result = chain.invoke({"prompt": prompt})
            duration = time.time() - start_time

            logger.debug(
                "LLM调用成功",
                attempt=attempt + 1,
                duration=f"{duration:.2f}s",
                result_type=type(result).__name__,
            )
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.warning(
                "LLM调用失败",
                attempt=attempt + 1,
                error=str(e),
                duration=f"{duration:.2f}s",
            )

            if attempt == 2:  # Last attempt
                logger.error("LLM调用最终失败", error=str(e))
                raise
            time.sleep(0.5 * (2**attempt))  # 0.5s, 1s backoff

    # This should never be reached, but added for type safety
    raise RuntimeError("Failed to get response after all retry attempts")
