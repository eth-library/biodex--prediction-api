from django.db import models
# from django_mysql.models import JSONField
from django.contrib.auth.models import User

from taxonomy.models import Species

class Image(models.Model):

    filename = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    # image_metadata = JSONField(null=True)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    species = models.ForeignKey(Species, null=False, on_delete=models.SET_NULL)