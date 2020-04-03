from django.core.exceptions import ValidationError


def validate_file_size(value):
    print(value)
    file_size = value.size
    if file_size > 429916160:
        raise ValidationError("The maximum file size that can be uploaded is 500MB")
    else:
        return value


def price_validator(value):
    if value < 0:
        raise ValidationError("price should be greater or equal 0")
    else:
        return True
