from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from taxonomy.models import Species

User = get_user_model()


class Image(models.Model):

    class ImageType(models.TextChoices):
        MOBILE = 'm', _('Mobile')
        DIGITIZATION = 'd', _('Digitization')

    def image_directory_path(instance, filename):
    # function to dynamically create the file save path 
    # file will be uploaded to MEDIA_ROOT/image/<collection_name>/<date>/<filename>

        if instance.collection is None:
            collection_name = ''

        date_fldr = instance.added_date.strftime('%Y_%m_%d')
        path = 'image/{0}/{1}/'.format(collection_name, date_fldr)

        return os.normpath(path)


    image = models.ImageField('uploaded image', upload_to=image_directory_path)
    added_date = models.DateTimeField('datetime image was added to application', auto_now=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    collection = models.CharField(max_length=200, blank=True, null=True) # name of collection that the image is from
    copyright = models.CharField(max_length=200, blank=True, null=True)
    image_type = models.CharField(max_length=1,
                                choices=ImageType.choices,
                                default=ImageType.MOBILE)
    specimen_id = models.CharField(max_length=100, null=True, blank=True) # barcode for identifying physical specimen in the image
    processed_git_uid = models.CharField(max_length=40, blank=True) # git short hash code (first 7 digits) for what code version was used to process images, if null, image has not been processed (git rev-parse --short HEAD)
    gbif_id = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['added_date','image']

    def __str__(self):
        return "{}".format(self.image)

