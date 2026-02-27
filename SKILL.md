---
name: gems-analyzer
description: |
  基于价值投资理念的AI投资分析系统，专为中文股票市场（A股和港股）设计。
  使用时机：
  1. 用户需要分析A股或港股的投资价值时（如"分析茅台股票"、"腾讯投资价值"）
  2. 用户询问股票估值指标（PE、PB、ROE、股息率等）时
  3. 用户需要基于巴菲特价值投资理念的股票分析报告时
  4. 用户需要获取股票实时行情或财务数据时
  5. 命令行工具以 gems-analyzer 开头时
---

# Gems Analyzer - AI价值投资分析工具

基于LangChain和价值投资理念的股票分析系统，支持A股和港股。

## 快速开始

### 1. 配置API密钥

```bash
cp env.example .env
# 编辑 .env 文件，添加以下任一API密钥：
# DEEPSEEK_API_KEY=your-deepseek-api-key
# 或
# USE_QWEN=true
# DASHSCOPE_API_KEY=your-dashscope-api-key
```

### 2. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 3. 开始分析

```bash
# 分析单只股票
gems-analyzer 600519

# 分析港股
gems-analyzer 00700.HK

# 交互式分析
gems-analyzer --interactive
```

## 使用方式

### 方式一：快速单次分析（推荐）

适用于快速获取单只股票的投资分析报告。

```bash
# 分析A股
gems-analyzer 600519

# 分析港股
gems-analyzer 00700.HK

# 输出JSON格式
gems-analyzer 600519 --json

# 指定数据源
gems-analyzer 600519 --source akshare

# 强制重新分析（忽略缓存）
gems-analyzer 600519 --force
```

### 方式二：交互式深度分析

适用于多轮对话、深度追问的场景。

```bash
gems-analyzer --interactive
```

交互模式提示词示例：
- "分析茅台的护城河"
- "对比茅台和五粮液的估值"
- "腾讯的分红情况如何"

### 方式三：批量分析

同时分析多只股票并生成对比报告。

```bash
# 批量分析
gems-analyzer --batch 600519 000858 00700.HK

# 输出到文件
gems-analyzer --batch 600519 000858 --output report.md
```

## 股票代码格式

| 市场 | 格式示例 | 说明 |
|-----|---------|------|
| A股上海 | `600519.SH` 或 `600519` | 6开头为上海主板 |
| A股深圳 | `000001.SZ` 或 `000001` | 0开头为深圳主板 |
| A股创业板 | `300750.SZ` 或 `300750` | 3开头为创业板 |
| 港股 | `00700.HK` 或 `00700` | 需带.HK后缀或自动识别 |

股票代码模糊匹配规则：
- 纯数字6开头 → 自动添加 `.SH`
- 纯数字0/3开头 → 自动添加 `.SZ`
- 包含.HK或纯数字5位 → 识别为港股

## 输出格式说明

### Markdown报告（默认）

包含以下章节：
1. **股票基本信息** - 代码、名称、当前价格
2. **好生意分析** - 护城河、管理层、业务模式、现金流
3. **好价格分析** - PE/PB估值、ROE、安全边际
4. **投资建议** - 综合评估、仓位建议、风险提示

### JSON结构化数据

```json
{
  "symbol": "600519.SH",
  "stock_name": "贵州茅台",
  "current_price": 1600.00,
  "valuation": {
    "pe_ratio": 28.5,
    "pb_ratio": 8.2,
    "roe": 28.0,
    "dividend_yield": 1.5
  },
  "business_quality": "excellent",
  "price_assessment": "fair",
  "recommendation": "适合长期持有"
}
```

## 缓存策略

系统自动缓存分析结果24小时。

缓存命中时的处理：
1. **提示用户**："该股票24小时内已分析过，使用缓存结果"
2. **询问用户**："是否重新分析获取最新数据？(y/n)"
3. **强制刷新**：`gems-analyzer 600519 --force`

## 故障排除

| 问题 | 解决方案 |
|-----|---------|
| API密钥错误 | 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 或 `DASHSCOPE_API_KEY` |
| 数据源连接失败 | 尝试切换数据源：`--source akshare` 或 `--source tdx` |
| 股票代码找不到 | 使用 `gems-analyzer --search 茅台` 搜索正确代码 |
| 分析结果为空 | 检查网络连接，或查看日志 |

## 参考资源

- **股票代码速查**：参见 [references/stock_codes.md](references/stock_codes.md)
- **估值指标说明**：参见 [references/valuation_guide.md](references/valuation_guide.md)
- **API详细文档**：参见 [references/api_reference.md](references/api_reference.md)

## 项目结构

```
gems-analyzer/
├── SKILL.md                    # 核心指导文档
├── scripts/
│   ├── gems-analyzer           # 主入口命令
│   ├── analyze_stock.py        # 核心分析脚本
│   ├── search_stock.py         # 股票搜索脚本
│   └── batch_analyze.py        # 批量分析脚本
├── references/
│   ├── stock_codes.md          # 常用股票代码速查
│   ├── valuation_guide.md      # 估值指标说明
│   └── api_reference.md        # API详细文档
├── assets/
│   └── report_template.md      # 分析报告模板
├── pyproject.toml              # Python项目配置
├── env.example                 # 环境变量示例
└── README.md                   # 项目文档
```

## 核心功能模块

| 模块 | 功能 | 路径 |
|-----|------|------|
| 数据源管理 | 多数据源自动切换和故障转移 | `gems/data_sources/` |
| AI Agent | 基于LangChain的任务规划和执行 | `gems/agent.py` |
| 估值计算 | PE/PB/ROE等核心指标计算 | `gems/api.py` |
| 缓存系统 | 多级缓存优化响应速度 | `gems/cache/` |
| 日志系统 | 结构化日志记录 | `gems/logging/` |

## 价值投资框架

基于巴菲特和段永平的投资理念：

### 好生意（Good Business）
- **护城河** - 品牌、成本、转换成本、网络效应
- **管理层** - 质量评估、股东利益一致性
- **业务模式** - 简单易懂、聚焦主业
- **现金流** - 自由现金流、现金储备

### 好价格（Good Price）
- **PE估值** - 市盈率相对历史区间
- **PB估值** - 市净率与净资产质量
- **ROE指标** - 净资产收益率持续性
- **安全边际** - 价格相对内在价值的折扣

## 开发指南

### 代码质量

```bash
# 格式化代码
black scripts/ src/

# 检查类型
mypy src/

# 运行测试
pytest

# 代码检查
ruff check scripts/ src/
```

### 添加新功能

1. **新数据源**：在 `gems/data_sources/` 实现 `DataSource` 抽象基类
2. **新分析工具**：创建脚本放入 `scripts/`，遵循现有错误处理模式
3. **新模型支持**：在 `gems/model.py` 添加模型配置

## 许可证

MIT License

---

**💎 Gems Analyzer - 让价值投资更智能！**
