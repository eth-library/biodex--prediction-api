from django.db import models
from taxonomy.models import Species


class PredModel(models.Model):
    # Tensorflow Models used for predictions
    # name should be the time that the model was created/trained formatted: YYYYMMDDHHmm eg 202005301230
    name = models.IntegerField(unique=True)
    date_added = models.DateTimeField(auto_now=True) # date that the model was added to Django. Not the date that it was made/trained.
    description = models.CharField(max_length=200, unique=False, null=True, blank=True)
    #values for image rgb mean and standard deviation. Used in prediction preprocessing
    rgb_mean_values = models.CharField(max_length=200, null=False, blank=False, default="[0, 0, 0]")
    stddev_rgb_values = models.CharField(max_length=200, null=False, blank=False, default="[1, 1, 1]")
    # species_key_map: maps the species as numbered by the prediction model, to the species PKs in the database
    species_key_map = models.CharField(max_length=50000, blank=False, null=False) #save json as text for dev purposes,switch to mysql native json serializer later
    #class_hierarchy_map: maps how classes in each hierarchical level map to the classes in their parent level
    class_hierarchy_map = models.CharField(max_length=50000, blank=False, null=False) #save json as text for dev purposes, switch to mysql native json serializer later
    #encoded_hierarchy: array with all levels of the hierarchy encoded. Used for sorting
    encoded_hierarchy = models.CharField(max_length=50000, blank=False, null=False) #save json as text for dev purposes, switch to mysql native json serializer later

    def __str__(self):
        return "{}: {}".format(str(self.name), str(self.description[:100]+'...'))