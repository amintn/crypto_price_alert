from django.db import models

from alert_user.models import AlertUser


class Exchange(models.Model):
    name = models.CharField(max_length=64)
    get_price_url = models.URLField(
        max_length=256,
        help_text="API endpoint of the exchange for getting price of a symbol pair. "
        "Symbols in the URL should be replaced with '{}' to be filled later. "
        "For example 'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={}-{}' for Kucoin exchange",
    )
    extract_price_keys = models.CharField(
        max_length=128,
        help_text="Dictionary keys seperated by dash, used to extract price from json response of get_price_url. "
        "For example 'data-price' keys for json response of {'data': {'price': 30}}",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower().capitalize()
        self.full_clean()
        return super().save(*args, **kwargs)


class SymbolPair(models.Model):
    first_symbol = models.CharField(
        max_length=8,
        help_text="First symbol of a pair that replaces the first '{}' of pair's exchange.get_price_url. "
        "For example 'BTC' for 'BTC-USDT' pair",
    )
    second_symbol = models.CharField(
        max_length=8,
        help_text="Second symbol of a pair that replaces the second '{}' of pair's exchange.get_price_url. "
        "For example 'USDT' for 'BTC-USDT' pair",
    )
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=14, decimal_places=8)

    def __str__(self):
        return f"{self.first_symbol}-{self.second_symbol}-{self.exchange.name}"

    def save(self, *args, **kwargs):
        self.first_symbol = self.first_symbol.upper()
        self.second_symbol = self.second_symbol.upper()
        self.full_clean()
        return super().save(*args, **kwargs)


class Rule(models.Model):
    RELATION_TO_TARGET_PRICE = (
        ("<=", "Alert if current_price <= target_price"),
        (">=", "Alert if current_price >= target_price"),
    )
    alert_user = models.ForeignKey(AlertUser, on_delete=models.CASCADE)
    symbol_pair = models.ForeignKey(SymbolPair, on_delete=models.PROTECT)
    action = models.CharField(max_length=2, choices=RELATION_TO_TARGET_PRICE)
    target_price = models.DecimalField(max_digits=14, decimal_places=8)

    def __str__(self):
        return f"{str(self.symbol_pair)} {self.action} {self.target_price}"

    def __repr__(self):
        return f"{self.alert_user.email}-{str(self)}"

    def is_reached(self) -> bool:
        """Returns True if this rule has reached its target price, returns False otherwise"""
        return eval(f"{self.symbol_pair.current_price} {self.action} {self.target_price}")
