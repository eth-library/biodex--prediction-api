from django.db import models
from django.contrib.auth import get_user_model

from taxonomy.models import Species

User = get_user_model()


class ImageLabelled(models.Model):
    image = models.ImageField('uploaded image', upload_to='labelled')
    specieskey = models.ForeignKey(Species,on_delete=models.SET_NULL, null=True)
    added_date = models.DateTimeField('datetime added to table', auto_now=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    copyright = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['added_date', 'specieskey__name']
        
    def __str__(self):
        return "{} : {}".format(self.image.name, self.specieskey.name)