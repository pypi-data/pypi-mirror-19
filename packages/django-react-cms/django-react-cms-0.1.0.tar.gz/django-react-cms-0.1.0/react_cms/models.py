from django.db import models

class ContentResource(models.Model):
  name = models.CharField("Resource Name", max_length=100)
  path = models.CharField("Resource Path", max_length=1000)
  json = models.TextField("Label", blank=True, null=True)

