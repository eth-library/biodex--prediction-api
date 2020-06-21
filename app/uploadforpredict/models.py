from django.db import models


class PredictImage(models.Model):
    image = models.ImageField('uploaded image for prediction',upload_to='image/prediction_uploads' )
    upload_date = models.DateTimeField('datetime uploaded for prediction', auto_now=True)
    
    def __str__(self):
        return str(self.image.name)