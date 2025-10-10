from django.db import models


class Reset(models.Model):
    phone = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)