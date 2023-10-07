from django.db import models


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
