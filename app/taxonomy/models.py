from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Family(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{} '.format(self.name)


class Subfamily(models.Model):

    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(Family, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{} '.format(self.name)


class Genus(models.Model):

    name = models.CharField(max_length=100, unique=False)
    parent = models.ForeignKey(Subfamily, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'parent')
        ordering = ['name']

    def __str__(self):
        return '{} '.format(self.name)


class Species(models.Model):

    name = models.CharField(max_length=100, unique=False)
    parent = models.ForeignKey(Genus, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,models.SET_NULL, blank=True, null=True)
    
    class Meta:
        unique_together = ('name', 'parent') # combination of Genus and species (known as epithet) must be unique
        ordering = ['name']

    def __str__(self):
        return '{} {}'.format(self.parent.name, self.name)
