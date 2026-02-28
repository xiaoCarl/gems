# Gems - A股和港股价值投资分析工具

## 概述

Gems是一个基于tushare和akshare的A股和港股价值投资分析工具，提供全面的股票基本面分析、估值指标计算和投资建议。该工具旨在帮助投资者进行价值投资决策，通过量化分析识别具有投资价值的股票。

## 功能特性

### 核心功能
1. **多市场支持**: 同时支持A股和港股市场分析
2. **实时数据**: 通过tushare和akshare获取实时行情数据
3. **财务分析**: 完整的财务报表分析（利润表、资产负债表、现金流量表）
4. **估值模型**: 多种估值模型计算（PE、PB、PS、PEG、DCF等）
5. **投资建议**: 基于多因子模型的智能投资建议
6. **风险提示**: 自动识别财务风险和市场风险

### 技术特性
1. **模块化设计**: 清晰的模块划分，易于扩展和维护
2. **缓存机制**: 智能缓存减少API调用，提高性能
3. **配置驱动**: 支持环境变量和配置文件多种配置方式
4. **完整日志**: 详细的日志记录，便于调试和监控
5. **多种输出格式**: 支持文本、JSON、HTML、PDF等多种输出格式

## 快速开始

### 环境要求
- Python 3.8+
- tushare token（需要注册获取）
- 网络连接（用于获取实时数据）

### 安装步骤
```bash
# 进入skill目录
cd /path/to/gems

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，添加你的tushare token
```

### 基本使用
```python
# 导入分析器
from src.analysis.value_investing import ValueInvestingAnalyzer

# 创建分析器
analyzer = ValueInvestingAnalyzer()

# 分析A股股票
result = analyzer.analyze_stock("000001", market="A")
print(result.summary())

# 分析港股股票
result = analyzer.analyze_stock("00700", market="HK")
print(result.summary())
```

## 项目结构

```
gems/
├── src/                    # 源代码目录
│   ├── data_sources/      # 数据源模块
│   ├── analysis/          # 分析模块
│   ├── utils/            # 工具模块
│   └── cli.py            # 命令行接口
├── scripts/               # 脚本目录
├── references/            # 参考文档
├── assets/               # 资源文件
├── requirements.txt      # Python依赖
├── .env.example          # 环境变量示例
├── SKILL.md             # 技能说明（本文件）
└── README.md            # 项目说明
```

## 详细文档

### 数据源
- **tushare**: A股数据接口，提供股票基本信息、财务数据、行情数据
- **akshare**: 港股数据接口，提供港股基本信息、财务数据、行情数据

### 分析方法
1. **估值分析**: PE、PB、PS、PEG、股息率等指标计算
2. **财务分析**: ROE、ROA、毛利率、负债率、流动比率等分析
3. **成长性分析**: 营收增长率、净利润增长率、净资产增长率
4. **综合评分**: 基于多因子模型的股票综合评分

### 投资建议
- **评分系统**: 0-100分综合评分
- **建议等级**: 强烈买入、买入、持有、卖出、强烈卖出
- **理由生成**: 自动生成推荐理由和风险提示
- **报告输出**: 支持文本、JSON、HTML格式报告

## 使用示例

### 示例1: 单只股票分析
```python
from src.analysis.value_investing import ValueInvestingAnalyzer

analyzer = ValueInvestingAnalyzer()
result = analyzer.analyze_stock("000001", market="A")

# 输出文本摘要
print(result.summary())

# 输出JSON格式
import json
print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

# 生成HTML报告
html_report = analyzer.generate_report(result, "html")
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_report)
```

### 示例2: 批量分析
```python
from src.analysis.value_investing import ValueInvestingAnalyzer

analyzer = ValueInvestingAnalyzer()
symbols = ["000001", "000002", "600519"]  # 平安银行、万科A、贵州茅台
results = analyzer.batch_analyze(symbols, market="A")

# 按评分排序输出
for i, result in enumerate(results, 1):
    print(f"{i}. {result.name} ({result.symbol}): {result.overall_score:.1f}分 - {result.recommendation.value}")
```

### 示例3: 命令行使用
```bash
# 分析单只股票
python src/cli.py analyze 000001 --market A

# 批量分析
python src/cli.py batch-analyze --file stocks.txt --market HK

# 生成报告
python src/cli.py report 00700 --market HK --output report.html
```

## 配置说明

### 环境变量配置
创建`.env`文件：
```env
# tushare配置（必填）
TUSHARE_TOKEN=your_tushare_token_here

# 缓存配置（可选）
CACHE_ENABLED=true
CACHE_TTL=3600

# 日志配置（可选）
LOG_LEVEL=INFO
LOG_FILE=logs/gems.log

# 分析阈值配置（可选）
ANALYSIS_PE_THRESHOLD=20
ANALYSIS_PB_THRESHOLD=2
ANALYSIS_ROE_THRESHOLD=15
```

### 配置文件
也可以通过`config.yaml`进行配置（详见assets/config.yaml）：
```yaml
data_sources:
  tushare:
    token: your_tushare_token_here
    timeout: 30

analysis:
  weights:
    valuation: 0.4
    financial: 0.4
    growth: 0.2
```

## 开发指南

### 代码规范
```bash
# 代码格式化
black src

# 代码检查
flake8 src

# 类型检查
mypy src
```

### 测试
```bash
# 运行测试
pytest tests/

# 生成测试覆盖率报告
pytest --cov=src --cov-report=html
```

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 免责声明

本工具仅供学习和研究使用，不构成投资建议。股市有风险，投资需谨慎。使用者应自行承担投资风险，作者不对任何投资损失负责。

## 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues: [项目Issues页面](https://github.com/yourusername/gems/issues)
- Email: your.email@example.com