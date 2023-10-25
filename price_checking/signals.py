from django.db.models.signals import post_init
from django.dispatch import receiver

from price_checking.models import Exchange


@receiver(post_init, sender=Exchange)
def add_extract_method(instance, **kwargs):
    keys = instance.json_keys_to_extract_price_from_request.split("-")

    def extract_price(response_dictionary):
        unravel = response_dictionary
        for key in keys:
            unravel = unravel.get(key)
        return unravel

    instance.extract_price = extract_price
