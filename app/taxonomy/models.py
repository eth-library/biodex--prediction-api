from django.db import models

# Create your models here.



class Family(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now=True)


class Subfamily(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(Family, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)


class Genus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(Subfamily, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)


class Species(models.Model):

    name = models.CharField(max_length=100, unique=False)
    parent = models.ForeignKey(Genus, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'parent') # combination of Genus and species (known as epithet) must be unique