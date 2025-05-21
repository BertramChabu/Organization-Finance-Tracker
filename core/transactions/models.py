from django.db import models

# Create your models here.
class Transactions(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50]