from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator


class Offkey(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.DecimalField(max_digits=3, decimal_places=0,
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100)
                                   ])
    active = models.BooleanField()

    def __str__(self):
        return self.code
