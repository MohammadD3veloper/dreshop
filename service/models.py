from django.conf import settings
from django.db import models

# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=500)
    to_supporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_send = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_user.username
