from django.db import models

from .steps import StepField


# 自訂的 QuerySet 類別，用於操作 ActiveQueryset 物件
class ActiveQueryset(models.QuerySet):
    def isActive(self):
        return self.filter(is_active=True)


# 股票模型
class Stock(models.Model):
    symbol = models.CharField(max_length=5, default="", unique=True)
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")
    sector = models.CharField(max_length=50, default="")
    slug = models.SlugField(unique=True, default="")
    is_active = models.BooleanField(default=True)

    # 使用 ActiveQueryset 作為 Manager，以方便查詢
    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return f"{self.symbol}"


# 歷史資料模型
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

    class Meta:
        unique_together = ("stock", "date")


# 回測策略模型
class BackTesting(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="backTesting"
    )
    name = models.CharField(max_length=30, default="")
    date = models.DateField(default="")
    strategyNumber = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"<{self.stock.symbol}> {self.strategyNumber} : {self.name}"

    def save(self, *args, **kwargs):
        if self._state.adding or not self.strategyNumber:
            last_strategy = (
                BackTesting.objects.filter(stock=self.stock)
                .order_by("-strategyNumber")
                .first()
            )
            self.strategyNumber = (
                0 if not last_strategy else last_strategy.strategyNumber + 1
            )
        super().save(*args, **kwargs)


# 回測步驟模型
class StrategySteps(models.Model):
    backTesting = models.ForeignKey(
        BackTesting, on_delete=models.CASCADE, related_name="strategySteps"
    )
    name = models.CharField(max_length=30, default="")
    strategyNumber = models.IntegerField(default=0)
    step = StepField(unique_for_field="backTesting", blank=True)  # 使用 AutoField 來自動增加

    def __str__(self):
        return f"{self.backTesting} 策略:{self.strategyNumber} 步驟:{self.step} 技術指標: {self.name}"
