from django.db import models

# Create your models here.

class RestorePassRequest(models.Model):
    email = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    hashaddr = models.CharField(max_length=255)

    def __unicode__(self):
        return self.text

