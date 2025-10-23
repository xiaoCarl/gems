import time

from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool

from gems.cache.manager import cache_manager
from gems.logging import get_logger

# 使用真实LLM API
from gems.model import call_llm
from gems.output.core import get_output_engine
from gems.prompts import (
    ACTION_SYSTEM_PROMPT,
    PLANNING_SYSTEM_PROMPT,
    STOCK_CONFIRMATION_PROMPT,
    TOOL_ARGS_SYSTEM_PROMPT,
    VALIDATION_SYSTEM_PROMPT,
    VALUE_INVESTMENT_ANSWER_PROMPT,
)
from gems.schemas import (
    Answer,
    IsDone,
    OptimizedToolArgs,
    StockConfirmation,
    Task,
    TaskList,
)
from gems.tools import TOOLS


class Agent:
    def __init__(self, max_steps: int = 20, max_steps_per_task: int = 5):
        self.max_steps = max_steps  # global safety cap
        self.max_steps_per_task = max_steps_per_task
        self.output = get_output_engine()
        self.logger = get_logger("agent")

    # ---------- task planning ----------
    def plan_tasks(self, query: str) -> list[Task]:
        self.logger.debug("开始任务规划", query=query)

        tool_descriptions = "\n".join(
            [
                f"- {getattr(t, 'name', 'unknown')}: {getattr(t, 'description', 'No description')}"
                for t in TOOLS
            ]
        )
        prompt = f"""
        Given the user query: "{query}",
        Create a list of tasks to be completed.
        Example: {{"tasks": [{{"id": 1, "description": "some task", "done": false}}]}}
        """
        system_prompt = PLANNING_SYSTEM_PROMPT.format(tools=tool_descriptions)

        start_time = time.time()
        try:
            self.logger.log_llm_call_start(prompt, system_prompt)
            response = call_llm(
                prompt, system_prompt=system_prompt, output_schema=TaskList
            )
            duration = time.time() - start_time
            self.logger.log_llm_call_end(response, duration)

            tasks = response.tasks
            self.logger.debug("任务规划完成", task_count=len(tasks))
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_llm_call_error(e, duration)
            tasks = [Task(id=1, description=query, done=False)]

        task_dicts = [task.dict() for task in tasks]
        self.output.show_tasks(task_dicts)
        return tasks

    # ---------- ask LLM what to do ----------
    def ask_for_actions(self, task_desc: str, last_outputs: str = "") -> AIMessage:
        self.logger.debug(
            "请求下一步行动",
            task_description=task_desc,
            last_outputs_length=len(last_outputs),
        )

        # last_outputs = textual feedback of what we just tried
        prompt = f"""
        We are working on: "{task_desc}".
        Here is a history of tool outputs from the session so far: {last_outputs}

        Based on the task and the outputs, what should be the next step?
        """

        start_time = time.time()
        try:
            self.logger.log_llm_call_start(prompt, ACTION_SYSTEM_PROMPT)
            # Convert TOOLS to BaseTool if needed
            tools_list = [t for t in TOOLS if isinstance(t, BaseTool)]
            response = call_llm(
                prompt, system_prompt=ACTION_SYSTEM_PROMPT, tools=tools_list
            )
            duration = time.time() - start_time
            self.logger.log_llm_call_end(response, duration)
            return response
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_llm_call_error(e, duration)
            self.logger.error("请求下一步行动失败", error=str(e))
            return AIMessage(content="Failed to get actions.")

    # ---------- ask LLM if task is done ----------
    def ask_if_done(self, task_desc: str, recent_results: str) -> bool:
        self.logger.debug(
            "检查任务是否完成",
            task_description=task_desc,
            recent_results_length=len(recent_results),
        )

        prompt = f"""
        We were trying to complete the task: "{task_desc}".
        Here is a history of tool outputs from the session so far: {recent_results}

        Is the task done?
        """

        start_time = time.time()
        try:
            self.logger.log_llm_call_start(prompt, VALIDATION_SYSTEM_PROMPT)
            resp = call_llm(
                prompt, system_prompt=VALIDATION_SYSTEM_PROMPT, output_schema=IsDone
            )
            duration = time.time() - start_time
            self.logger.log_llm_call_end(resp, duration)
            self.logger.debug(
                "任务完成状态检查", task_description=task_desc, done=resp.done
            )
            return resp.done
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_llm_call_error(e, duration)
            self.logger.error("任务完成状态检查失败", error=str(e))
            return False

    # ---------- optimize tool arguments ----------
    def optimize_tool_args(
        self, tool_name: str, initial_args: dict, task_desc: str
    ) -> dict:
        """Optimize tool arguments based on task requirements."""
        self.logger.debug(
            "优化工具参数", tool_name=tool_name, task_description=task_desc
        )

        tool = next((t for t in TOOLS if getattr(t, "name", None) == tool_name), None)
        if not tool:
            self.logger.warning("未找到工具", tool_name=tool_name)
            return initial_args

        # Get tool schema info
        tool_description = getattr(tool, "description", "No description")
        tool_schema = getattr(tool, "args_schema", None)
        if tool_schema and hasattr(tool_schema, "schema"):
            tool_schema = tool_schema.schema()
        else:
            tool_schema = {}

        prompt = f"""
        Task: "{task_desc}"
        Tool: {tool_name}
        Tool Description: {tool_description}
        Tool Parameters: {tool_schema}
        Initial Arguments: {initial_args}
        
        Review the task and optimize the arguments to ensure all relevant parameters are used correctly.
        Pay special attention to filtering parameters that would help narrow down results to match the task.
        """

        start_time = time.time()
        try:
            self.logger.log_llm_call_start(prompt, TOOL_ARGS_SYSTEM_PROMPT)
            response = call_llm(
                prompt,
                system_prompt=TOOL_ARGS_SYSTEM_PROMPT,
                output_schema=OptimizedToolArgs,
            )
            duration = time.time() - start_time
            self.logger.log_llm_call_end(response, duration)

            # Handle case where LLM returns dict directly instead of OptimizedToolArgs
            if isinstance(response, dict):
                optimized_args = response if response else initial_args
            else:
                optimized_args = response.arguments

            self.logger.debug(
                "工具参数优化完成",
                tool_name=tool_name,
                initial_args_count=len(initial_args),
                optimized_args_count=len(optimized_args),
            )
            return optimized_args
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_llm_call_error(e, duration)
            self.logger.error("工具参数优化失败", error=str(e))
            return initial_args

    # ---------- tool execution ----------
    def _execute_tool(self, tool, tool_name: str, inp_args):
        """Execute a tool with progress indication."""
        self.logger.log_tool_call_start(tool_name, inp_args)
        start_time = time.time()

        try:
            self.output.show_progress(f"执行工具: {tool_name}")
            result = tool.run(inp_args)
            duration = time.time() - start_time

            self.logger.log_tool_call_end(tool_name, result, duration)
            self.output.show_progress(f"工具执行完成: {tool_name}")
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_tool_call_error(tool_name, e, duration)
            raise

    # ---------- confirm action ----------
    def confirm_action(self, tool: str, input_str: str) -> bool:
        # In production you'd ask the user; here we just log and auto-confirm
        # Risky tools are not implemented in this version.
        return True

    # ---------- main loop ----------
    def run(self, query: str) -> str:
        """
        Executes the main agent loop to process a user query.

        This method orchestrates the entire process of understanding a query,
        planning tasks, executing tools to gather information, and synthesizing
        a final answer.

        Args:
            query: The user's natural language query.

        Returns:
            A comprehensive answer to the user's query.
        """
        # Display the user's query
        confirmed, code = self._confirm_stock_info(query)

        # 如果股票信息需要澄清，返回等待重新输入
        if not confirmed or code is None:
            return "需要重新输入股票信息"

        # 在股票确认后、计划任务前检查缓存
        if code:
            cached_result = cache_manager.get_analysis_result(code)
            if cached_result:
                self.logger.info("缓存命中", symbol=code, query=query)
                self.output.show_progress(f"从缓存中获取 {code} 的分析结果")
                self.output.show_answer(cached_result, "value_investment")

                return cached_result
            else:
                self.logger.debug("缓存未命中", symbol=code, query=query)

        # Initialize agent state for this run.
        step_count = 0
        last_actions: list[str] = []
        session_outputs: list[str] = []

        # 1. Decompose the user query into a list of tasks.
        tasks = self.plan_tasks(query)

        # If no tasks were created, the query is likely out of scope.
        if not tasks:
            answer = self._generate_answer(query, session_outputs)
            self.output.show_answer(answer, "value_investment")
            return answer

        # 2. Execute tasks until all are complete or max steps are reached.
        while any(not t.done for t in tasks):
            # Global safety break.
            if step_count >= self.max_steps:
                self.logger.warning("达到全局最大步数限制，中止执行")
                break

            # Select the next incomplete task.
            task = next(t for t in tasks if not t.done)
            self.logger.log_task_start(task.description)
            self.output.show_progress(f"开始执行: {task.description}")

            # Loop for a single task, with its own step limit.
            per_task_steps = 0
            task_outputs: list[str] = []
            while per_task_steps < self.max_steps_per_task:
                if step_count >= self.max_steps:
                    self.logger.warning("达到全局最大步数限制，停止执行")
                    return

                # Ask the LLM for the next action to take for the current task.
                ai_message = self.ask_for_actions(
                    task.description, last_outputs="\n".join(task_outputs)
                )

                # If no tool is called, the task is considered complete.
                if not hasattr(ai_message, "tool_calls") or not ai_message.tool_calls:
                    task.done = True
                    self.output.show_progress(f"完成: {task.description}")
                    break

                # Process each tool call returned by the LLM.
                tool_calls = getattr(ai_message, "tool_calls", [])
                for tool_call in tool_calls:
                    if step_count >= self.max_steps:
                        break

                    tool_name = tool_call["name"]
                    initial_args = tool_call["args"]

                    # Refine tool arguments for better performance.
                    optimized_args = self.optimize_tool_args(
                        tool_name, initial_args, task.description
                    )

                    # Create a signature of the action to be taken.
                    action_sig = f"{tool_name}:{optimized_args}"

                    # Detect and prevent repetitive action loops.
                    last_actions.append(action_sig)
                    if len(last_actions) > 4:
                        last_actions = last_actions[-4:]
                    if len(set(last_actions)) == 1 and len(last_actions) == 4:
                        print("Detected repeating action — aborting to avoid loop.")
                        return

                    # Execute the tool.
                    tool_to_run = next(
                        (t for t in TOOLS if getattr(t, "name", None) == tool_name),
                        None,
                    )
                    if tool_to_run and self.confirm_action(
                        tool_name, str(optimized_args)
                    ):
                        try:
                            result = self._execute_tool(
                                tool_to_run, tool_name, optimized_args
                            )
                            output = f"Output of {tool_name} with args {optimized_args}: {result}"
                            session_outputs.append(output)
                            task_outputs.append(output)
                        except Exception as e:
                            print(f"Tool execution failed: {e}")
                            error_output = f"Error from {tool_name} with args {optimized_args}: {e}"
                            session_outputs.append(error_output)
                            task_outputs.append(error_output)
                    else:
                        print(f"Invalid tool: {tool_name}")

                    step_count += 1
                    per_task_steps += 1

                # After a batch of tool calls, check if the task is complete.
                if self.ask_if_done(task.description, "\n".join(task_outputs)):
                    task.done = True
                    self.logger.log_task_end(task.description, True)
                    self.output.show_progress(f"完成: {task.description}")
                    break

        # 3. Synthesize the final answer from all collected tool outputs.
        answer = self._generate_answer(query, session_outputs)
        self.output.show_answer(answer, "value_investment")

        # 将分析结果存入缓存
        if code:
            try:
                cache_manager.set_analysis_result(code, answer)
                self.logger.info("分析结果已缓存", symbol=code, query=query)
            except Exception as e:
                self.logger.warning("缓存存储失败", symbol=code, error=str(e))

        return answer

    # ---------- answer generation ----------
    def _generate_answer(self, query: str, session_outputs: list) -> str:
        """Generate the final answer based on collected data."""
        self.logger.debug(
            "生成最终答案", query=query, session_outputs_count=len(session_outputs)
        )

        all_results = (
            "\n\n".join(session_outputs)
            if session_outputs
            else "No data was collected."
        )
        answer_prompt = f"""
        Original user query: "{query}"
        
        Data and results collected from tools:
        {all_results}
        
        Based on the data above, provide a comprehensive value investment analysis.
        Structure your answer around the two core dimensions of value investing:
        
        1. Good Business (好生意)
           - Moat Analysis (护城河)
           - Management Quality (管理层质量) 
           - Business Simplicity (业务简单易懂)
           - Free Cash Flow (自由现金流)
        
        2. Good Price (好价格)
           - PE Valuation (市盈率估值)
           - PB Valuation (市净率估值) 
           - ROC Metrics (资本回报率)
           - Margin of Safety (安全边际)
        
        For each dimension, provide:
        - Clear assessment (优秀/良好/一般/较差)
        - Specific data and analysis
        - Key supporting metrics
        - Risk factors
        
        Conclude with an overall investment recommendation including:
        - Whether it meets "good business + good price" criteria
        - Suggested position sizing
        - Key risks to monitor
        - Long-term holding value assessment
        """

        start_time = time.time()
        try:
            self.logger.log_llm_call_start(
                answer_prompt, VALUE_INVESTMENT_ANSWER_PROMPT
            )
            answer_obj = call_llm(
                answer_prompt,
                system_prompt=VALUE_INVESTMENT_ANSWER_PROMPT,
                output_schema=Answer,
            )
            duration = time.time() - start_time
            self.logger.log_llm_call_end(answer_obj, duration)
            self.logger.debug("答案生成完成", answer_length=len(answer_obj.answer))
            return answer_obj.answer
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_llm_call_error(e, duration)
            self.logger.error("答案生成失败", error=str(e))
            return "抱歉，生成答案时出现错误。"

    def _confirm_stock_info(self, query: str):
        """确认用户输入的股票信息"""
        self.logger.debug("确认股票信息", query=query)

        confirmation_prompt = f"""
        用户查询: "{query}"

        请确认股票信息并输出确认信息。
        """

        start_time = time.time()
        try:
            self.logger.log_llm_call_start(
                confirmation_prompt, STOCK_CONFIRMATION_PROMPT
            )
            # 使用LLM确认股票信息
            confirmation = call_llm(
                confirmation_prompt,
                system_prompt=STOCK_CONFIRMATION_PROMPT,
                output_schema=StockConfirmation,
            )
            duration = time.time() - start_time
            self.logger.log_llm_call_end(confirmation, duration)

            # 显示确认信息
            if confirmation.clarification_needed:
                self.logger.debug(
                    "需要澄清股票信息", clarification=confirmation.clarification_needed
                )
                print(f"   {confirmation.clarification_needed}")
                return False, None  # 需要重新输入
            else:
                self.logger.debug(
                    "股票信息确认成功",
                    stock_name=confirmation.stock_name,
                    stock_code=confirmation.stock_code,
                )
                print(
                    f"  Gems-agent将对股票#{confirmation.stock_code}#进行价值投资分析，请稍侯"
                )
                print()
                return True, confirmation.stock_code  # 确认成功

        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_llm_call_error(e, duration)
            self.logger.error("股票信息确认失败", error=str(e))
            # 如果确认失败，显示默认信息
            print(" 输入信息，无法处理")
            print()
            return False, None  # 需要重新输入
