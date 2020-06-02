from django.db import models


class PredictImage(models.Model):
    image = models.ImageField('uploaded image for prediction', )
    upload_date = models.DateTimeField('datetime uploaded for prediction', auto_now=True)
    