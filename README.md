# Gems 🤖 价值投资分析智能体

Gems 是一个自主的价值投资研究智能体，能够自动规划任务、收集财务数据并生成投资分析报告。

## 快速开始

### 安装

#### 方法一：通过 npm 安装（推荐）
```bash
npm install -g gems-agent
```

#### 方法二：从源码安装
```bash
git clone https://github.com/xiaoCarl/gems.git
cd gems
uv sync
```

### 配置

1. 复制环境变量文件：
```bash
cp env.example .env
```

2. 在 `.env` 文件中设置 API 密钥：
```bash
# DeepSeek API（默认）
DEEPSEEK_API_KEY=your-deepseek-api-key

# 或使用 Qwen API
USE_QWEN=true
DASHSCOPE_API_KEY=your-dashscope-api-key
```

### 使用

```bash
# 通过 npm 安装
npm install -g gems-agent
gems-agent

# 或从源码运行
uv run gems-agent
```

## 功能特性

### 🎯 核心能力
- **智能任务规划** - 自动分解复杂投资问题
- **自主数据收集** - 获取实时行情和财务数据
- **价值投资分析** - 基于好生意+好价格框架
- **安全执行** - 内置循环检测和步骤限制

### 📊 数据源
- **通达信API** - 实时行情数据（A股/港股）
- **AkShare** - 财务数据（利润表、资产负债表、现金流量表）

### 🤖 支持模型
- **DeepSeek**（默认）- 设置 `DEEPSEEK_API_KEY`
- **Qwen** - 设置 `USE_QWEN=true` 和 `DASHSCOPE_API_KEY`

## 使用示例

输入股票相关问题，例如：
- "贵州茅台的市盈率和市净率是多少？"
- "分析宁德时代的财务健康状况"
- "腾讯控股的价值投资分析"

Gems 将自动：
1. 规划研究任务
2. 收集财务数据
3. 执行分析计算
4. 生成投资报告

## 价值投资框架

Gems 基于经典价值投资理念，专注于：

### 好生意
- 护城河分析
- 管理层质量
- 业务简单易懂
- 自由现金流

### 好价格
- 市盈率估值
- 市净率估值
- 资本回报率
- 安全边际

## 项目结构

```
gems/
├── src/gems/
│   ├── agent.py          # 主智能体
│   ├── model.py          # LLM 模型接口
│   ├── data_sources/     # 数据源管理
│   ├── tools/           # 分析工具
│   └── output/          # 输出引擎
├── tests/               # 测试文件
└── docs/               # 文档
```

## 贡献

欢迎贡献！请：
1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

MIT License
