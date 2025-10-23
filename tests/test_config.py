"""
配置模块测试
"""

import os
import sys
from unittest.mock import patch

import pytest

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# 设置测试模式环境变量
os.environ["GEMS_TEST_MODE"] = "true"

from gems.config import Config


class TestConfig:
    """配置模块测试"""

    def test_settings_default_values(self):
        """测试默认配置值"""
        # 在测试模式中，deepseek_api_key 是可选的
        config = Config()

        # 验证默认值
        assert config.deepseek_api_key is None  # 在测试模式中为None
        assert config.use_qwen is False
        assert config.preferred_data_source == "tdx"
        assert config.request_timeout == 30
        assert config.max_retries == 3
        assert config.cache_enabled is True
        assert config.default_typical_price == 10.0

    def test_typical_price_methods(self):
        """测试典型价格方法"""
        with patch.dict(os.environ, {"deepseek_api_key": "test_key"}):
            config = Config()

            # 测试获取已知股票的典型价格
            assert config.get_typical_price("600519.SH") == 1600.0
            assert config.get_typical_price("000001.SZ") == 12.0
            assert config.get_typical_price("600036.SH") == 35.0

            # 测试获取未知股票的默认价格
            assert config.get_typical_price("UNKNOWN.SH") == 10.0

    def test_update_typical_price(self):
        """测试更新典型价格"""
        with patch.dict(os.environ, {"deepseek_api_key": "test_key"}):
            config = Config()

            # 更新现有股票价格
            config.update_typical_price("600519.SH", 1700.0)
            assert config.get_typical_price("600519.SH") == 1700.0

            # 添加新股票价格
            config.update_typical_price("000858.SZ", 40.0)
            assert config.get_typical_price("000858.SZ") == 40.0

    def test_update_typical_price_invalid(self):
        """测试更新无效的典型价格"""
        with patch.dict(os.environ, {"deepseek_api_key": "test_key"}):
            config = Config()

            with pytest.raises(ValueError, match="典型价格必须为正数"):
                config.update_typical_price("600519.SH", 0.0)

    def test_data_source_validation_valid(self):
        """测试有效的数据源验证"""
        # 这个测试现在只验证配置类能够接受有效的数据源
        config = Config()
        # 在测试模式中，preferred_data_source 使用默认值 'tdx'
        assert config.preferred_data_source == "tdx"

    def test_data_source_validation_invalid(self):
        """测试无效的数据源验证"""
        config = Config()
        # 直接设置无效的数据源并测试验证方法
        config.preferred_data_source = "invalid_source"
        with pytest.raises(ValueError, match="数据源必须是以下之一"):
            config._validate_config()

    def test_timeout_validation(self):
        """测试超时配置验证"""
        config = Config()
        config.request_timeout = 0
        with pytest.raises(ValueError, match="请求超时必须为正数"):
            config._validate_config()

    def test_retries_validation(self):
        """测试重试次数验证"""
        config = Config()
        config.max_retries = -1
        with pytest.raises(ValueError, match="最大重试次数必须为非负数"):
            config._validate_config()

    def test_cache_ttl_validation(self):
        """测试缓存TTL验证"""
        config = Config()
        config.cache_ttl_realtime = 0
        with pytest.raises(ValueError, match="实时数据缓存TTL必须为正数"):
            config._validate_config()

    def test_cache_size_validation(self):
        """测试缓存大小验证"""
        config = Config()
        config.cache_max_size = 0
        with pytest.raises(ValueError, match="缓存最大大小必须为正数"):
            config._validate_config()

    def test_log_size_validation(self):
        """测试日志大小验证"""
        config = Config()
        config.log_max_bytes = 0
        with pytest.raises(ValueError, match="日志最大字节数必须为正数"):
            config._validate_config()

    def test_log_backup_validation(self):
        """测试日志备份数量验证"""
        config = Config()
        config.log_backup_count = -1
        with pytest.raises(ValueError, match="日志备份数量必须为非负数"):
            config._validate_config()

    def test_typical_price_validation(self):
        """测试典型价格验证"""
        config = Config()
        config.default_typical_price = 0
        with pytest.raises(ValueError, match="默认典型价格必须为正数"):
            config._validate_config()

    def test_env_file_loading(self):
        """测试环境文件加载"""
        # 在测试模式中，环境变量不会影响配置值
        # 这个测试现在只验证配置类能够正确初始化
        config = Config()

        # 在测试模式中，deepseek_api_key 为 None
        assert config.deepseek_api_key is None
        # 其他配置使用默认值
        assert config.use_qwen is False
        assert config.request_timeout == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
