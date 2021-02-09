from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

# Create your models here.
class Entry(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	pre_bp_sys = models.IntegerField()
	pre_bp_dia = models.IntegerField()
	pre_weight = models.IntegerField()
	post_bp_sys = models.IntegerField()
	post_bp_dia = models.IntegerField()
	post_weight = models.IntegerField()
	date_created = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return str(self.user) + ': ' + self.date_created.strftime('%m/%d/%Y')

class Image(models.Model):
	image = models.ImageField()
	entry = models.OneToOneField(Entry,on_delete=models.CASCADE)

