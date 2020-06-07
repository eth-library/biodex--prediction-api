from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from image.models import Image
from taxonomy.models import Family, Subfamily, Genus, Species

User = get_user_model()

class ImageClassification(models.Model):

    class UserTypes(models.TextChoices):
        STUDENT = 'ST', _('Student')
        EXPERT = 'EX', _('Expert')

    image_key = models.ForeignKey(Image, blank=False, null=False, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)
    user_type = models.CharField(
        max_length=2,
        choices=UserTypes.choices,
        default=UserTypes.STUDENT)
    family_key = models.ForeignKey(Family, on_delete=models.PROTECT)
    subfamily_key = models.ForeignKey(Subfamily, on_delete=models.PROTECT)
    genus_key = models.ForeignKey(Genus, on_delete=models.PROTECT)
    species_key = models.ForeignKey(Species, on_delete=models.PROTECT)