#!/usr/bin/env python3
"""
Test script to demonstrate paginated task list display
"""

from gems.gli.logger import GLILogger

# Create test tasks to test pagination
test_tasks = [
    {"id": 1, "description": "分析贵州茅台的护城河特征", "done": True, "priority": "high"},
    {"id": 2, "description": "评估管理层质量和诚信度", "done": False, "priority": "high"},
    {"id": 3, "description": "计算自由现金流指标和稳定性", "done": False, "priority": "medium"},
    {"id": 4, "description": "计算PE、PB、ROC等估值比率", "done": False, "priority": "medium"},
    {"id": 5, "description": "评估业务简单性和可理解性", "done": False, "priority": "low"},
    {"id": 6, "description": "分析行业竞争格局和市场份额", "done": False, "priority": "medium"},
    {"id": 7, "description": "评估公司治理结构和股东权益保护", "done": False, "priority": "medium"},
    {"id": 8, "description": "分析财务健康状况和偿债能力", "done": False, "priority": "high"},
    {"id": 9, "description": "评估研发投入和技术创新能力", "done": False, "priority": "low"},
    {"id": 10, "description": "分析ESG表现和可持续发展能力", "done": False, "priority": "low"},
    {"id": 11, "description": "进行敏感性分析和情景测试", "done": False, "priority": "medium"},
    {"id": 12, "description": "制定投资建议和风险控制策略", "done": False, "priority": "high"}
]

print("🎯 测试计划任务分页显示功能")
print("=" * 60)

logger = GLILogger()

print("\n📋 测试分页显示 (12个任务，每页8个，共2页):")
logger.log_task_list(test_tasks)

print("\n✅ 分页显示功能测试完成")
print("\n功能特点:")
print("• 每页显示8个任务")
print("• 显示任务状态图标 (✅ 完成 / ⏳ 待执行)")
print("• 显示页码信息 (第1页/共2页)")
print("• 显示任务总数统计")
print("• 提供滚动查看提示")