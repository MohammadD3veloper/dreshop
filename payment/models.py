from django.db import models
from django.conf import settings


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True, blank=True
    )
    amount = models.FloatField()
    description = models.TextField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    authority = models.CharField(max_length=200, null=True, blank=True)
    ref_id = models.CharField(max_length=200, null=True, blank=True)
    card_pan = models.CharField(max_length=200, null=True, blank=True)
    card_hash = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
