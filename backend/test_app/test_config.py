from app.config import (
    BaseConfig,
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
    config_by_name,
)


def test_config_mapping_contains_expected_environments():
    assert config_by_name["development"] is DevelopmentConfig
    assert config_by_name["testing"] is TestingConfig
    assert config_by_name["production"] is ProductionConfig


def test_base_config_defaults_are_defined():
    assert BaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert BaseConfig.MAX_CONTENT_LENGTH == 16 * 1024 * 1024
    assert "pdf" in BaseConfig.ALLOWED_EXTENSIONS


def test_testing_config_flags_are_set():
    assert TestingConfig.TESTING is True
    assert TestingConfig.JWT_ACCESS_TOKEN_EXPIRES is False


def test_production_config_debug_is_disabled():
    assert ProductionConfig.DEBUG is False
