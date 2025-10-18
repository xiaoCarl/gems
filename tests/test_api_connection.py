"""
测试DeepSeek API连接
"""

import os
import sys
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 加载环境变量
load_dotenv()

# 检查API密钥
api_key = os.getenv('DEEPSEEK_API_KEY')
print(f"API密钥配置: {'已设置' if api_key else '未设置'}")

if api_key:
    print(f"API密钥长度: {len(api_key)}")
    print(f"API密钥前10位: {api_key[:10]}...")
    
    try:
        # 测试导入模型
        from gems.model import call_llm
        print("✅ 模型导入成功")
        
        # 测试简单的API调用
        print("🧪 测试API连接...")
        response = call_llm("你好，请简单回复'测试成功'")
        print(f"✅ API调用成功: {response}")
        
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ 未找到DEEPSEEK_API_KEY环境变量")