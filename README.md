# Gems 💎 AI投资分析助手

基于价值投资理念的AI投资分析系统，专为中文股票市场（A股和港股）设计。

## 🌟 核心特性

- **🤖 AI驱动分析** - 基于LangChain和深度学习的智能分析
- **💎 价值投资框架** - 遵循巴菲特投资理念：好生意 + 好价格
- **📊 多数据源整合** - AkShare、通达信、Yahoo Finance等数据源
- **🌐 实时数据获取** - 股价、财务数据、估值指标
- **💬 智能对话界面** - Web界面和命令行双模式支持
- **⚡ 高性能缓存** - 混合缓存系统优化响应速度

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/xiaoCarl/gems.git
cd gems

# 安装依赖
uv sync

# 或者使用pip
pip install -e .
```

### 配置

1. 复制环境变量文件：
```bash
cp env.example .env
```

2. 编辑 `.env` 文件，设置API密钥：
```bash
# DeepSeek API（推荐）
DEEPSEEK_API_KEY=your-deepseek-api-key

# 或者使用Qwen API
USE_QWEN=true
DASHSCOPE_API_KEY=your-dashscope-api-key
```

### 启动

#### Web界面模式（推荐）
```bash
# 启动Web服务器
./start.sh web

# 访问 http://localhost:8000
```

#### 命令行模式
```bash
# 启动CLI
./start.sh cli
```

#### API服务模式
```bash
# 启动API服务器
./start.sh api 8080
```

## 📁 项目结构

```
gems/
├── apps/                    # 应用程序入口
│   ├── cli/                # 命令行界面
│   ├── servers/            # Web服务器
│   └── web/                # Web前端
├── src/                    # 核心源码
│   └── gems/               # 主要包
│       ├── agent.py        # AI智能体
│       ├── api.py          # 统一API接口
│       ├── cli.py          # 命令行接口
│       ├── config.py       # 配置管理
│       ├── data_sources/   # 数据源管理
│       ├── tools/          # 分析工具
│       └── logging.py      # 日志系统
├── docs/                   # 文档
├── logs/                   # 日志文件
├── tests/                  # 测试代码
├── static/                 # 静态资源
├── start.sh               # 统一启动脚本
├── pyproject.toml         # Python项目配置
└── README.md              # 项目文档
```

## 💡 使用示例

### Web界面
1. 打开浏览器访问 `http://localhost:8000`
2. 在输入框中输入股票相关问题：
   - "分析茅台股票"
   - "600519的投资价值"
   - "腾讯控股怎么样"
3. 获得专业的价值投资分析报告

### 命令行
```bash
# 分析股票
$ gems
> 分析茅台股票

# 获取帮助
$ gems --help
```

### API调用
```bash
# 搜索股票
curl "http://localhost:8000/api/stocks/search?q=茅台"

# 获取股票详情
curl "http://localhost:8000/api/stocks/600519.SH"

# 智能体分析
curl -X POST "http://localhost:8000/api/agent/analyze" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "600519.SH", "analysis_type": "comprehensive"}'
```

## 🎯 价值投资框架

基于巴菲特和段永平的价值投资理念：

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

## 🔧 开发

### 代码质量
```bash
# 格式化代码
black apps/ src/ tests/

# 检查类型
mypy src/

# 运行测试
pytest

# 代码检查
ruff check apps/ src/
```

### 项目配置
- **代码格式化**: Black + isort
- **类型检查**: MyPy
- **代码检查**: Ruff
- **测试框架**: Pytest

## 📊 数据源

- **AkShare** - A股和港股财务数据
- **通达信** - 实时行情数据
- **Yahoo Finance** - 港股和国际股票数据
- **混合缓存** - 提升数据获取性能

## 🛡️ 安全特性

- **输入验证** - 严格的参数验证
- **错误处理** - 完善的异常处理机制
- **日志记录** - 详细的操作日志
- **连接管理** - WebSocket连接安全

## 📚 文档

- [项目架构](docs/ARCHITECTURE.md) - 技术架构说明
- [WebSocket设置](docs/WEBSOCKET_SETUP.md) - WebSocket配置
- [界面优化](docs/INTERFACE_OPTIMIZATION_SUMMARY.md) - 界面设计

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
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [DeepSeek](https://deepseek.com/) - AI模型支持

---

**💎 Gems - 让价值投资更智能！**

专注于价值投资分析，助您做出更明智的投资决策。"file_path":"/Users/caihui/caihui/gems/README.md