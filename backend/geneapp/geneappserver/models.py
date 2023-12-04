from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class Sample(models.Model):
    name= models.CharField(max_length=100)
    local_path= models.CharField(max_length=100, blank=True, null=True)
    acession= models.CharField(max_length=100, blank=True, null=True)

class Projeto(models.Model):

    LBS = [('SP', 'SHORT_PAIRED'), ('SS', 'SHORT_SINGLE'), ('LS', 'LONG_SINGLE')]
    name= models.CharField(max_length=100)
    control= models.CharField(max_length=100)
    treatment= models.CharField(max_length=100)
    path= models.CharField(max_length=100, blank=True, null=True)
    organism= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    genome= models.CharField(max_length=100, blank=True, null=True)
    online = models.BooleanField(default=False)
    anotattion= models.CharField(max_length=200)
    proteome= models.CharField(max_length=200)
    transcriptome= models.CharField(max_length=200)
    ctrl_samples: models.ForeignKey(Sample, on_delete=models.CASCADE)
    treat_samples: models.ForeignKey(Sample, on_delete=models.CASCADE)
    library: models.CharField(max_length=2, choices=LBS)

    threads: models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(100)])
    ram:  models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(100)])
    disk:  models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    fast: models.BooleanField(default=False)
    qvalue: models.FloatField(default=.05, validators=[MinValueValidator(0), MaxValueValidator(1)])
    psi: models.FloatField(default=.1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.nome