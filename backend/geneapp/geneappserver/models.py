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


class Command(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.CharField(max_length=50, blank=True, null=True)
    ended_at = models.CharField(max_length=50, blank=True, null=True)
    op=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    tsp=models.PositiveIntegerField(default=0, validators=[MaxValueValidator(999999)])
    lock=models.PositiveIntegerField(default=0, validators=[MaxValueValidator(999999)])
    arg1=models.CharField(max_length=200, blank=True, null=True)
    arg2=models.CharField(max_length=200, blank=True, null=True)
    arg3=models.CharField(max_length=200, blank=True, null=True)
    arg4=models.CharField(max_length=200, blank=True, null=True)
    arg5=models.CharField(max_length=200, blank=True, null=True)
    arg6=models.CharField(max_length=200, blank=True, null=True)
    arg7=models.CharField(max_length=200, blank=True, null=True)
    arg8=models.CharField(max_length=200, blank=True, null=True)
    arg9=models.CharField(max_length=200, blank=True, null=True)
    
    end=models.BooleanField(default=False)
    status=models.CharField(max_length=100, blank=True, null=True)
    success=models.BooleanField(default=False)
    
    meta=models.CharField(max_length=999, blank=True, null=True)
    info=models.CharField(max_length=999, blank=True, null=True)
    out=models.CharField(max_length=999, blank=True, null=True)
    log=models.CharField(max_length=999, blank=True, null=True)
    err=models.CharField(max_length=999, blank=True, null=True)
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)
                                   
    def __str__(self):
        s = 'S' if self.success else 'E' if self.end else 'W'
        return f"{self.id}|{self.tsp}[{s}: {self.op} - {self.status} / {self.project} ] {self.arg1} {self.arg2} {self.arg3} {self.arg4} ..."

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
    rmats_readLength= models.FloatField(default=.1, validators=[MinValueValidator(20), MaxValueValidator(500)])
    
    @property
    def samples(self):
        return Sample.objects.filter(project=self)
    
    @property
    def commands(self):
        return Command.objects.filter(project=self)

    def __str__(self):
        return f"[{self.id}] {self.name}: {self.path}"
    
