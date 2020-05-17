from django.db import models
from card.models import CardModel
from django.db.models.signals import pre_save, post_save
from sec_academy.utilities.create_unique_fields import unique_id_generator_orders
# Create your models here.
ORDER_CHOICES = (
  ('created', 'Created'),
  ('paid', 'Paid'),
  ('refunded', 'Refunded'),
  ('cancel', 'Cancel'),
)

class OrdersModel(models.Model):
  order_id  = models.CharField(max_length=120, blank=True, unique=True,)
  card      = models.OneToOneField(CardModel, on_delete=models.CASCADE)
  status    = models.CharField(max_length=30, blank=True, choices=ORDER_CHOICES, default="created")
  total     = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

  def __str__(self):
    return self.order_id

  class Meta:
    verbose_name        = "Order"
    verbose_name_plural = "Orders"   


def create_custom_order_id(instance, sender, *args, **kwargs):
  if not instance.order_id:
    instance.order_id= unique_id_generator_orders(instance)

pre_save.connect(create_custom_order_id, sender=OrdersModel)
  
# def post_total_from_card(instance, sender, created, *args, **kwargs):
#   if created:
#     instance.update_total()
#     # instance.check_seats()

# post_save.connect(post_total_from_card, sender=OrdersModel)

