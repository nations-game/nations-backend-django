from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CharField, 
    FloatField, 
    ForeignKey, 
    IntegerField, 
    Model, 
    CASCADE
)

class NationFactory(Model):
    nation = ForeignKey("Nation", on_delete=CASCADE, related_name="factories")
    factory_type = CharField(max_length=100)

    ticks_run = IntegerField(
        default=3,
        validators=[
            MaxValueValidator(24)
        ]
    )