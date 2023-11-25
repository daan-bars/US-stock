from django.db import models


# 股票
class Stock(models.Model):
    symbol = models.CharField(max_length=5, default="")
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")
    sector = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"<{self.symbol}>: {self.name}"


# 歷史資料
class Historical(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="Historical"
    )
    date = models.DateField(default="")
    open = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    volume = models.IntegerField(default=0)

    def __str__(self):
        return f"<{self.stock.symbol}>: {self.date} O:{self.open} H:{self.high} L:{self.low} C:{self.close} V:{self.volume}"
