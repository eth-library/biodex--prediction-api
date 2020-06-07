from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from taxonomy.models import Species

User = get_user_model()


class Image(models.Model):

    class ImageType(models.TextChoices):
        MOBILE = 'm', _('Mobile')
        DIGITIZATION = 'd', _('Digitization')

    image = models.ImageField('uploaded image', upload_to='image')
    image_date = models.DateTimeField('date image was taken', blank=True, null=True)
    added_date = models.DateTimeField('datetime image was added to application', auto_now=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    copyright = models.CharField(max_length=200, blank=True, null=True)
    image_type = models.CharField(max_length=1,
                                choices=ImageType.choices,
                                default=ImageType.MOBILE)
    
    class Meta:
        ordering = ['added_date','image']

    def __str__(self):
        return "{} : {}".format(self.image.name)