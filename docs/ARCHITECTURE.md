# Gems 项目架构文档

## 项目结构

```
src/gems/
├── __init__.py              # 包初始化
├── config.py                # 配置管理
├── exceptions.py            # 自定义异常
├── logging.py               # 统一日志记录
├── api.py                   # 统一API接口
├── data_sources/            # 数据源抽象层
│   ├── __init__.py
│   ├── akshare_source.py    # AkShare数据源
│   ├── yfinance_source.py   # yfinance数据源
│   └── manager.py           # 数据源管理器
├── tools/                   # LangChain工具
│   ├── __init__.py
│   ├── financials.py        # 财务数据工具
│   ├── analysis.py          # 分析工具
│   ├── filings.py           # 文件工具
│   └── tdx_api.py           # 通达信API（待重构）
├── utils/                   # 工具函数
│   ├── __init__.py
│   └── intro.py
├── output/                  # 输出处理
│   ├── __init__.py
│   ├── core.py
│   └── logger.py
├── agent.py                 # AI代理
├── cli.py                   # 命令行接口
├── model.py                 # 模型配置
├── prompts.py               # 提示词
└── schemas.py               # 数据模式
```

## 核心架构

### 1. 数据源抽象层

新的架构引入了数据源抽象层，支持多种数据源：

- **AkShareDataSource**: 主要数据源，支持A股和港股的财务数据和实时数据
- **YFinanceDataSource**: 备用数据源，主要用于港股实时数据

### 2. 数据源管理器

`DataSourceManager` 负责：
- 管理多个数据源实例
- 根据股票类型自动选择最优数据源
- 提供数据源故障转移机制
- 统一错误处理和日志记录

### 3. 配置管理

`Config` 类提供统一的配置管理：
- 环境变量读取
- 配置验证
- 默认值设置

### 4. 统一日志记录

`Logger` 类提供：
- 统一的日志格式
- 可配置的日志级别
- 结构化日志输出

### 5. 自定义异常

定义了清晰的异常层次：
- `GemsError`: 基础异常
- `DataSourceError`: 数据源相关异常
- `FinancialDataError`: 财务数据异常
- `ConfigurationError`: 配置异常

## 数据源选择策略

### 实时数据
- **A股**: 优先使用配置的数据源，备用AkShare
- **港股**: 优先使用yfinance，备用AkShare

### 财务数据
- **A股和港股**: 统一使用AkShare

## 使用示例

```python
from gems.api import get_realtime_stock_data, get_stock_financials, get_stock_valuation_data

# 获取实时数据
realtime_data = get_realtime_stock_data('000001.SZ')  # A股
realtime_data = get_realtime_stock_data('00700.HK')   # 港股

# 获取财务数据
financial_data = get_stock_financials('000001.SZ', 'annual')

# 获取估值数据
valuation_data = get_stock_valuation_data('000001.SZ')
```

## 配置

环境变量：
```bash
PREFERRED_DATA_SOURCE=tdx  # 或 akshare
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

## 开发指南

### 添加新数据源

1. 在 `data_sources/` 目录下创建新数据源类
2. 实现 `DataSource` 抽象基类
3. 在 `manager.py` 中注册新数据源

### 错误处理

使用自定义异常类，提供清晰的错误信息：
```python
from gems.exceptions import DataSourceError, FinancialDataError

try:
    data = get_stock_financials(symbol, period)
except FinancialDataError as e:
    # 处理财务数据错误
    logger.error(f"财务数据获取失败: {e}")
```

### 日志记录

使用统一的日志记录器：
```python
from gems.logging import get_logger

logger = get_logger("module_name")
logger.info("操作成功", symbol=symbol, data_source=source)
logger.error("操作失败", error=str(e), symbol=symbol)
```