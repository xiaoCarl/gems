# Gems 快速参考指南

## 核心功能概览

### 1. 数据源
- **A股数据**: 通过tushare获取（需要token）
- **港股数据**: 通过akshare获取
- **模拟数据**: 简化版使用模拟数据

### 2. 分析功能
- **估值分析**: PE、PB、PS、股息率等
- **财务分析**: ROE、ROA、毛利率、负债率等
- **成长分析**: 营收增长、利润增长等
- **综合评分**: 0-100分评分系统

### 3. 输出格式
- **文本格式**: 简洁的文本摘要
- **JSON格式**: 结构化数据
- **HTML格式**: 美观的网页报告

## 快速使用示例

### Python API 使用
```python
from src.analysis.value_investing import ValueInvestingAnalyzer

# 创建分析器
analyzer = ValueInvestingAnalyzer()

# 分析单只股票
result = analyzer.analyze_stock("000001", market="A")
print(result.summary())

# 批量分析
results = analyzer.batch_analyze(["000001", "000002"], market="A")

# 生成报告
html_report = analyzer.generate_report(result, "html")
```

### 命令行使用
```bash
# 分析单只股票
python src/cli.py analyze 000001 --market A

# 批量分析
python src/cli.py batch-analyze 000001 000002 600519 --market A

# 生成HTML报告
python src/cli.py report 000001 --market A --output report.html
```

### 脚本使用
```bash
# 使用分析脚本
python scripts/analyze_a_stock.py --symbol 000001 --market A

# 运行演示
python scripts/value_investing_demo.py
```

## 配置说明

### 环境变量
创建 `.env` 文件：
```env
# tushare token（必填，实际使用时）
TUSHARE_TOKEN=your_token_here

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/gems.log

# 分析阈值
ANALYSIS_PE_THRESHOLD=20
ANALYSIS_PB_THRESHOLD=2
```

### 简化版说明
当前版本为简化版，特点：
1. 使用模拟数据，无需真实API调用
2. 无需安装外部依赖（tushare、akshare等）
3. 适合演示和测试
4. 实际使用时需要配置真实数据源

## 股票代码格式

### A股代码
- 上证股票: 6位数字，如 `600519`
- 深证股票: 6位数字，如 `000001`
- 系统会自动添加后缀（`.SH` 或 `.SZ`）

### 港股代码
- 5位数字，如 `00700`
- 直接使用数字代码

## 分析结果解读

### 评分系统
- **90-100分**: 强烈买入
- **80-89分**: 买入
- **60-79分**: 持有
- **40-59分**: 卖出
- **0-39分**: 强烈卖出

### 关键指标
- **PE (市盈率)**: <15 低估，15-25 合理，>25 高估
- **PB (市净率)**: <1 低估，1-2 合理，>2 高估
- **股息率**: >3% 有吸引力
- **ROE**: >15% 优秀

## 常见问题

### Q1: 如何获取tushare token？
A: 访问 https://tushare.pro/ 注册并获取token。

### Q2: 港股数据是否完整？
A: 简化版使用模拟数据，完整版需要akshare支持。

### Q3: 分析结果准确吗？
A: 简化版使用模拟数据，结果仅供参考。实际分析需要真实数据。

### Q4: 如何扩展功能？
A: 可以修改 `src/data_sources/` 中的类来连接真实数据源。

## 开发指南

### 项目结构
```
src/
├── data_sources/     # 数据源模块
├── analysis/         # 分析模块
├── utils/           # 工具模块
└── cli.py           # 命令行接口
```

### 添加新数据源
1. 在 `data_sources/` 中创建新类
2. 实现必要的方法
3. 在 `DataManager` 中注册

### 添加新分析指标
1. 在 `value_investing.py` 中添加计算方法
2. 更新 `AnalysisResult` 数据类
3. 更新评分逻辑

## 性能优化建议

### 数据缓存
- 启用缓存减少API调用
- 设置合理的缓存时间
- 定期清理缓存

### 批量处理
- 使用批量分析功能
- 合理设置并发数
- 避免频繁调用

### 错误处理
- 添加重试机制
- 记录详细日志
- 提供友好的错误信息

## 下一步计划

### 短期改进
1. 添加更多估值模型
2. 优化评分算法
3. 完善文档

### 长期规划
1. 支持更多数据源
2. 添加机器学习模型
3. 开发Web界面

## 联系与支持

- 问题反馈: 查看项目文档
- 功能建议: 提交Issue
- 贡献代码: 提交Pull Request

---

**注意**: 当前为简化版本，实际投资决策请谨慎，建议使用真实数据进行分析。