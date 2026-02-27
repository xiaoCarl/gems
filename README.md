# Gems Analyzer 💎

基于价值投资理念的AI投资分析系统，专为中文股票市场（A股和港股）设计。

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 核心特性

- **🤖 AI驱动分析** - 基于LangChain和DeepSeek/Qwen大模型的智能分析
- **💎 价值投资框架** - 遵循巴菲特投资理念：好生意 + 好价格
- **📊 多数据源整合** - AkShare实时数据，覆盖A股和港股
- **⚡ 高性能缓存** - 智能缓存系统优化响应速度
- **🔧 命令行工具** - 简洁高效的CLI交互体验

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/xiaoCarl/gems-analyzer.git
cd gems-analyzer

# 安装依赖（推荐uv）
uv sync

# 或使用pip
pip install -e .
```

### 配置API密钥

```bash
cp env.example .env
# 编辑.env文件，添加以下任一API密钥：

# 方式1: DeepSeek API（推荐）
DEEPSEEK_API_KEY=your-deepseek-api-key

# 方式2: 阿里云Qwen API
USE_QWEN=true
DASHSCOPE_API_KEY=your-dashscope-api-key
```

### 开始使用

```bash
# 分析单只股票
gems-analyzer 600519

# 分析港股
gems-analyzer 00700.HK

# 交互式分析模式
gems-analyzer --interactive

# 批量分析多只股
gems-analyzer --batch 600519 000858 00700.HK
```

## 📖 使用指南

### 作为Kimi CLI Skill使用

1. 安装Kimi CLI并配置
2. 将此项目添加到skills目录
3. Kimi会自动识别并调用相关功能

### 命令行用法

```bash
# 快速分析
gems-analyzer 600519                    # 分析贵州茅台
gems-analyzer 600519 --json             # 输出JSON格式
gems-analyzer 600519 --force            # 强制重新分析

# 搜索股票
gems-analyzer --search 茅台

# 批量分析
gems-analyzer --batch 600519 000858 --output report.md

# 交互式模式
gems-analyzer --interactive
```

### 股票代码格式

| 市场 | 格式示例 | 说明 |
|-----|---------|------|
| A股上海 | `600519.SH` 或 `600519` | 6开头为上海主板 |
| A股深圳 | `000001.SZ` 或 `000001` | 0开头为深圳主板 |
| A股创业板 | `300750.SZ` 或 `300750` | 3开头为创业板 |
| 港股 | `00700.HK` 或 `00700` | 需带.HK后缀或自动识别 |

## 💎 价值投资框架

### 好生意分析

- **护城河** - 品牌、成本、转换成本、网络效应
- **管理层** - 质量评估、股东利益一致性
- **业务模式** - 简单易懂、聚焦主业
- **现金流** - 自由现金流、现金储备

### 好价格分析

- **PE估值** - 市盈率相对历史区间
- **PB估值** - 市净率与净资产质量
- **ROE指标** - 净资产收益率持续性
- **安全边际** - 价格相对内在价值的折扣

## 📁 项目结构

```
gems-analyzer/
├── SKILL.md                    # Kimi CLI Skill定义
├── scripts/
│   ├── gems-analyzer           # 主入口命令
│   ├── analyze_stock.py        # 核心分析脚本
│   ├── search_stock.py         # 股票搜索脚本
│   └── batch_analyze.py        # 批量分析脚本
├── src/gems/                   # 核心Python包
│   ├── agent.py                # AI Agent核心
│   ├── api.py                  # 统一API接口
│   ├── model.py                # LLM模型配置
│   ├── config.py               # 配置管理
│   ├── data_sources/           # 数据源管理
│   ├── cache/                  # 缓存系统
│   └── tools/                  # 分析工具
├── references/                 # 参考文档
│   ├── stock_codes.md          # 股票代码速查
│   ├── valuation_guide.md      # 估值指标说明
│   └── api_reference.md        # API文档
├── assets/                     # 资源文件
│   └── report_template.md      # 报告模板
├── pyproject.toml              # 项目配置
└── README.md                   # 本文件
```

## 🔧 开发指南

### 代码质量

```bash
# 格式化代码
black scripts/ src/

# 类型检查
mypy src/

# 代码检查
ruff check scripts/ src/
```

### 添加新功能

1. **新数据源** - 在 `src/gems/data_sources/` 实现
2. **新分析工具** - 创建脚本放入 `scripts/`
3. **新模型支持** - 在 `src/gems/model.py` 添加配置

## 📝 示例输出

```markdown
# 贵州茅台 (600519.SH) 价值投资分析

## 核心估值指标

| 指标 | 数值 | 评估 |
|-----|------|------|
| PE | 21.39 | 合理偏低 |
| PB | 7.91 | 较高（品牌溢价）|
| ROE | 36.99% | 优秀 |
| 股息率 | 3.85% | 良好 |

## 好生意分析

### 护城河 - 极强 ⭐⭐⭐⭐⭐

茅台拥有多重护城河：
- 品牌护城河："国酒"地位，百年品牌积淀
- 供给侧壁垒：核心产区稀缺性
- 定价权：连续提价，毛利率91%+

## 投资建议

**评级：买入/持有**

当前PE 21.39倍处于历史合理区间下限，ROE 36.99%体现极强的盈利能力。
建议作为核心仓位长期持有。
```

## 🤝 贡献

欢迎贡献！请：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [LangChain](https://langchain.com/) - AI应用框架
- [AkShare](https://akshare.akfamily.xyz/) - 金融数据接口
- [DeepSeek](https://deepseek.com/) - AI模型支持

---

**💎 Gems Analyzer - 让价值投资更智能！**

专注于价值投资分析，助您做出更明智的投资决策。
