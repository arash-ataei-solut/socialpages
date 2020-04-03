from django.core.exceptions import ValidationError


def price_validator(value):
    if value < 0:
        raise ValidationError("price should be greater or equal 0")
    else:
        return True
