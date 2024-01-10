import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, F

from core.models import BaseModel
from foodmenu.models import Food
from offkey.models import Offkey
from tables.models import Table


# Create your models here.


class Order(BaseModel):
    status_fields = [("W", "Waiting"),
                     ("C", "Canceled"),
                     ("P", "Preparation"),
                     ("T", "Transmission"),
                     ("F", "Finished")]
    customer_phone = models.CharField(max_length=100, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=1, choices=status_fields, default='W')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name='orders')
    offkey = models.ForeignKey(Offkey,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.DecimalField(default=0.0, max_digits=3, decimal_places=2,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def __str__(self):
        return f"Order #{self.id} - {self.customer_phone} - {self.table}"


class OrderItem(BaseModel):
    """
    https://stackoverflow.com/questions/10655730/quantize-result-has-too-many-digits-for-current-context
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Food, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    def get_cost(self):
        return self.price * self.quantity
