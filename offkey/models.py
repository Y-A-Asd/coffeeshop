from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import BaseModel


class Offkey(BaseModel):
    """
        https://docs.djangoproject.com/en/5.0/ref/models/fields/
    """
    class Mode(models.TextChoices):
        OneTime = 'OT', _('OneTimeUse')
        TimeEvent = 'TE', _('MultiTimeUse')

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=1,
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100)
                                   ])
    active = models.BooleanField()
    mode = models.CharField(
        max_length=2,
        choices = Mode,
        default=Mode.TimeEvent
    )
    def __str__(self):
        return self.code
