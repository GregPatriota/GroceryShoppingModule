from django.db import models

# Create your models here.


class Countries(models.Model):
    country_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.country_name
