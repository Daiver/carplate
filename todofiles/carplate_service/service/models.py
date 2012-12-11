from django.db import models

# Create your models here.

class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField( max_length=128)
    reg_time = models.DateTimeField(auto_now=True)
    
    def set_password(self, raw_pass):
        import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)
        
class Picture(models.Model):
    pic_name = models.CharField(max_length=128)
    user = models.ForeignKey(User)
    add_time = models.DateTimeField(auto_now=True)
    vote = models.SmallIntegerField()
    ans = models.CharField(max_length=30)
    recognized = models.CharField(max_length=128)
    

    