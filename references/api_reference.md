# Gems API 参考

## 统一API接口

位于 `gems.api` 模块，提供数据获取的统一入口。

### get_realtime_stock_data

获取实时股票数据。

```python
from gems.api import get_realtime_stock_data

data = get_realtime_stock_data("600519.SH")
# 返回：
# {
#     "symbol": "600519.SH",
#     "name": "贵州茅台",
#     "current_price": 1600.00,
#     "open": 1590.00,
#     "high": 1620.00,
#     "low": 1585.00,
#     "prev_close": 1588.00,
#     "volume": 25000,
#     "turnover": 40000000,
#     "change_percent": 0.75
# }
```

### get_stock_financials

获取财务数据。

```python
from gems.api import get_stock_financials

data = get_stock_financials("600519.SH", period="annual")
# 返回：
# {
#     "income_statements": [...],      # 利润表
#     "balance_sheets": [...],         # 资产负债表
#     "cash_flow_statements": [...]    # 现金流量表
# }
```

### get_stock_valuation_data

获取估值数据（自动计算PE/PB/ROE等）。

```python
from gems.api import get_stock_valuation_data

data = get_stock_valuation_data("600519.SH")
# 返回：
# {
#     "symbol": "600519.SH",
#     "market": "A股",
#     "current_price": 1600.00,
#     "pe_ratio": 28.5,
#     "pb_ratio": 8.2,
#     "roe": 28.0,
#     "eps": 56.14,
#     "bvps": 195.12,
#     "dividend_yield": 1.5
# }
```

---

## Agent 系统

### Agent 类

位于 `gems.agent.Agent`。

```python
from gems.agent import Agent

# 创建Agent（CLI模式）
agent = Agent(use_web_output=False)

# 执行分析
result = agent.run("分析茅台股票的投资价值")
print(result)
```

### Agent 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|-------|------|
| max_steps | int | 20 | 全局最大执行步数 |
| max_steps_per_task | int | 5 | 每任务最大步数 |
| use_web_output | bool | False | 是否使用Web模式 |

---

## 数据源管理

### DataSourceManager

位于 `gems.data_sources.manager`。

```python
from gems.data_sources.manager import data_source_manager

# 获取实时数据
data = data_source_manager.get_realtime_data("600519.SH")

# 获取财务数据
data = data_source_manager.get_financial_data("600519.SH", period="annual")
```

### 数据源选择策略

| 市场 | 实时数据优先级 | 财务数据来源 |
|-----|---------------|-------------|
| A股 | TDX > AkShare | AkShare |
| 港股 | yfinance > AkShare | AkShare |

---

## 缓存系统

### CacheManager

位于 `gems.cache.manager`。

```python
from gems.cache.manager import cache_manager

# 获取缓存结果
result = cache_manager.get_analysis_result("600519.SH")

# 存储分析结果
cache_manager.set_analysis_result("600519.SH", analysis_result)

# 获取实时数据缓存
data = cache_manager.get_realtime_data("600519.SH")

# 获取财务数据缓存
data = cache_manager.get_financial_data("600519.SH", period="annual")
```

### 缓存TTL配置

| 数据类型 | TTL | 配置项 |
|---------|-----|-------|
| 实时数据 | 5分钟 | CACHE_TTL_REALTIME |
| 财务数据 | 1小时 | CACHE_TTL_FINANCIAL |
| 历史数据 | 24小时 | CACHE_TTL_HISTORICAL |
| 分析结果 | 24小时 | CACHE_TTL_ANALYSIS |

---

## 配置系统

### Config 类

位于 `gems.config`。

```python
from gems.config import get_config

config = get_config()

# 获取API密钥
deepseek_key = config.deepseek_api_key

# 获取数据源配置
preferred_source = config.preferred_data_source

# 获取典型价格（降级策略）
price = config.get_typical_price("600519.SH")
```

### 环境变量配置

```bash
# LLM API配置（必选其一）
DEEPSEEK_API_KEY=your-key
# 或
USE_QWEN=true
DASHSCOPE_API_KEY=your-key

# 数据源配置
PREFERRED_DATA_SOURCE=tdx  # 或 akshare

# 缓存配置
CACHE_ENABLED=true
CACHE_TTL_ANALYSIS=86400

# 日志配置
LOG_LEVEL=INFO
```

---

## 工具系统（Tools）

位于 `gems.tools`，LangChain工具集合。

### 可用工具列表

```python
from gems.tools import TOOLS

# 查看所有工具
for tool in TOOLS:
    print(f"{tool.name}: {tool.description}")
```

### 核心工具

| 工具名 | 功能 | 参数 |
|-------|------|------|
| get_stock_realtime | 获取实时行情 | symbol |
| get_stock_financials | 获取财务数据 | symbol, period |
| get_stock_valuation | 获取估值指标 | symbol |
| search_stock_by_name | 名称搜索股票 | name |

---

## 错误处理

### 异常类型

```python
from gems.exceptions import (
    GemsError,           # 基础异常
    DataSourceError,     # 数据源错误
    FinancialDataError,  # 财务数据错误
    ConfigurationError,  # 配置错误
)

try:
    data = get_stock_valuation_data("600519.SH")
except FinancialDataError as e:
    print(f"财务数据获取失败: {e}")
except DataSourceError as e:
    print(f"数据源错误: {e}")
```

---

## 日志系统

```python
from gems.logging import get_logger

logger = get_logger("my_module")

logger.info("操作成功", symbol="600519.SH")
logger.error("操作失败", error=str(e), symbol="600519.SH")
```
