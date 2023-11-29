import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestsStockModels:
    def test_str_method(self, stock_factory):
        # Arrange
        # Act
        x = stock_factory(symbol="AAPL", name="Apple")
        # Assert
        assert x.__str__() == "AAPL"


class TestHistoricalModels:
    def test_str_method(self, historical_factory):
        # Arrange
        # Act
        obj = historical_factory(
            stock__symbol="AAPL",
            date="2022-01-01",
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0,
            volume=100.0,
        )
        historical = obj
        # Assert
        assert (
            str(historical)
            == "<AAPL>: 2022-01-01 O:100.0 H:110.0 L:90.0 C:105.0 V:100.0"
        )


class TestBackTestingModels:
    def test_str_method(self, back_testing_factory):
        # Arrange
        # Act
        obj = back_testing_factory(
            stock__symbol="AAPL",
            name="策略1",
            date="2022-01-01",
            strategy_number=0,
            is_active=True,
        )
        # Assert
        assert obj.__str__() == "<AAPL> 0 : 策略1"


class TestStrategyStepsModels:
    def test_str_method(self, strategy_steps_factory):
        # Arrange
        # Act
        obj = strategy_steps_factory(description="步驟1")
        # Assert
        assert obj.__str__() == "步驟1"

    def test_duplicate_step_values(self, strategy_steps_factory, back_testing_factory):
        # Arrange
        # Act
        obj = back_testing_factory()
        strategy_steps_factory(step=0, back_testing=obj)
        with pytest.raises(ValidationError):
            strategy_steps_factory(step=0, back_testing=obj).clean()
        # Assert
