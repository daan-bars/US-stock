from rest_framework import serializers
from .models import Stock, Historical


class StockSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source="symbol")

    class Meta:
        model = Stock
        fields = ("name", "stock_symbol")


# class HistoricalListSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         transformed_data = {}
#         for item in data:
#             # 解析字串表示形式
#             parts = item.__str__().split(" ")

#             if len(parts) >= 2:
#                 stock_symbol = parts[0][1:-2]  # 提取股票符號，去除 '<' 和 '>'

#                 if stock_symbol not in transformed_data:
#                     transformed_data[stock_symbol] = []

#                 transformed_data[stock_symbol].append(
#                     {
#                         "date": parts[1],
#                         "open": float(parts[2][2:]),
#                         "high": float(parts[3][2:]),
#                         "low": float(parts[4][2:]),
#                         "close": float(parts[5][2:]),
#                         "volume": int(parts[6][2:]),
#                     }
#                 )
#         return transformed_data.items()


class HistoricalSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source="stock.symbol")
    # stock = StockSerializer()

    class Meta:
        model = Historical
        fields = ("stock_symbol", "date", "open", "high", "low", "close", "volume")
