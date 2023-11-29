from rest_framework import serializers
from .models import Stock, Historical, BackTesting, StrategySteps


class StockSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source="symbol")

    class Meta:
        model = Stock
        fields = ("name", "stock_symbol")


class HistoricalSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source="stock.symbol")

    class Meta:
        model = Historical
        fields = ("stock_symbol", "date", "open", "high", "low", "close", "volume")


class StrategyStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategySteps
        fields = ("description", "step")


class BackTestingSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source="stock.symbol")
    strategy_steps = StrategyStepsSerializer(many=True)

    class Meta:
        model = BackTesting
        exclude = ("is_active", "id", "stock")
