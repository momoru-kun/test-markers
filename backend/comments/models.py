from django.db import models
from markers.models import Picture


# Create your models here.
class Comment(models.Model):

    panorama = models.ForeignKey(
        to=Picture, 
        on_delete=models.CASCADE
    )
    ip_addr = models.GenericIPAddressField(
        verbose_name = "IP Адрес"
    )
    email = models.EmailField(
        verbose_name = "E-Mail"
    )
    text = models.TextField(
        verbose_name = "Коментарий", 
        max_length = 400
    )
    send_date = models.DateTimeField(
        verbose_name="Время отправки"
    )

    def __str__(self):
        return "<Comment from {}>".format(self.email)

    def to_dict(self):
        return {
            "email": self.email,
            "text": self.text,
            "send_date": self.send_date
        }