from django.contrib import admin

from taxonomy.models import Family, Subfamily, Genus, Species

admin.site.register(Family)
admin.site.register(Subfamily)
admin.site.register(Genus)
admin.site.register(Species)