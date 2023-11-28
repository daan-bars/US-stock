import pytest

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
