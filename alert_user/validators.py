from django.core.validators import ValidationError


def iran_mobile_phone_number_validator(number):
    if len(number) != 11:
        raise ValidationError("Phone number has invalid length")
    if not number.isdigit():
        raise ValidationError("Phone number has non digit characters")
    if number[:2] != "09" or number[2] not in ("0", "1", "2", "3", "9"):
        raise ValidationError("Phone number format is not correct")
