from django.apps import AppConfig
from django.db.models.signals import post_init
from django.dispatch import receiver


class PriceCheckingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "price_checking"

    def ready(self):
        @receiver(post_init, sender="price_checking.Exchange")
        def add_extract_method(instance, **kwargs):
            keys = instance.extract_price_keys.split("-")

            def extract_price(response_dictionary):
                unravel = response_dictionary
                for key in keys:
                    unravel = unravel.get(key)
                return unravel

            instance.extract_price = extract_price
