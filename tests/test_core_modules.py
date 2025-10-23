"""
核心模块测试脚本

测试核心模块的导入和基本功能，不依赖外部API。
"""

import os
import sys

# 设置测试模式环境变量
os.environ["GEMS_TEST_MODE"] = "true"

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_config_import():
    """测试配置模块导入"""
    from gems.config import Config

    assert Config is not None


def test_data_sources_import():
    """测试数据源模块导入"""
    from gems.data_sources.manager import DataSourceManager

    assert DataSourceManager is not None


def test_tools_import():
    """测试工具模块导入"""
    from gems.tools.analysis import analyze_moat_characteristics

    assert analyze_moat_characteristics is not None


def test_schemas_import():
    """测试数据模式导入"""
    from gems.schemas import Task, TaskList

    assert Task is not None
    assert TaskList is not None


if __name__ == "__main__":
    print("Gems 核心模块测试")
    print("=" * 50)

    test_config_import()
    test_data_sources_import()
    test_tools_import()
    test_schemas_import()

    print("\n" + "=" * 50)
    print("所有核心模块导入测试通过")
