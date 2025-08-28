# noinspection PyUnresolvedReferences
from django.core.exceptions import ValidationError

def validate_age(value):
    if value < 18 or value > 100:
        raise ValidationError('Возраст должен быть от 18 до 100 лет')

def validate_city(value):
    if len(value.strip()) < 2:
        raise ValidationError('Название города слишком короткое')