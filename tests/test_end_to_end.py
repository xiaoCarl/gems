"""
端到端测试脚本

测试重构后的简单输出系统是否能正常工作。
"""

import os
import sys

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_data_sources_import():
    """测试数据源模块导入"""
    from gems.data_sources.manager import DataSourceManager

    assert DataSourceManager is not None


def test_tools_import():
    """测试工具模块导入"""
    from gems.tools.analysis import analyze_moat_characteristics

    assert analyze_moat_characteristics is not None


def test_output_import():
    """测试输出模块导入"""
    from gems.output.core import SimpleOutputEngine

    assert SimpleOutputEngine is not None


if __name__ == "__main__":
    print("Gems Agent 端到端测试")
    print("=" * 50)

    test_data_sources_import()
    test_tools_import()
    test_output_import()

    print("\n" + "=" * 50)
    print("所有模块导入测试通过")
