from django.db import models

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=255)
    born_at = models.PositiveIntegerField(null=True, blank=True)
    friends = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name