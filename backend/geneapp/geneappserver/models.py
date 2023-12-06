from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class Sample(models.Model):
    name= models.CharField(max_length=50)
    acession= models.CharField(max_length=100)
    local_path= models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=20)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
                               
    def __str__(self):
        return self.name


class Project(models.Model):

    name= models.CharField(max_length=50)
    control= models.CharField(max_length=20)
    treatment= models.CharField(max_length=20)
    path= models.CharField(max_length=100, blank=True, null=True)
    organism= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    online = models.BooleanField(default=False)
    fast= models.BooleanField(default=False)
    status= models.PositiveIntegerField(default=1)

    genome= models.CharField(max_length=200)
    anotattion= models.CharField(max_length=200)
    proteome= models.CharField(max_length=200)
    transcriptome= models.CharField(max_length=200)
    library= models.CharField(max_length=20)

    threads= models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(100)])
    ram=  models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(100)])
    disk=  models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])

    qvalue= models.FloatField(default=.05, validators=[MinValueValidator(0), MaxValueValidator(1)])
    psi= models.FloatField(default=.1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    @property
    def samples(self):
        return Sample.objects.filter(project=self)

    def __str__(self):
        return self.name
    
