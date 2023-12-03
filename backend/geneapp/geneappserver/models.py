from django.db import models

# Create your models here.

class Gene(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    strand = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name