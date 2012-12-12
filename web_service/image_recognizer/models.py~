from django.db import models

class img2rec(models.Model):
	download_data = models.DateField()
	path = models.CharField(max_length = 4096)

class letter(models.Model):
	download_data = models.DateField()
	path = models.CharField(max_length = 4096)
	fk_img2rec = models.ForeignKey(img2rec)
