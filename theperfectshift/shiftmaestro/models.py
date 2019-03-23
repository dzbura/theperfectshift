from django.db import models
#from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.template.defaulttags import register

class Employee(models.Model):
	user = models.ForeignKey(User, default='0', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	position = models.CharField(max_length=31)
	schedulemaker = models.IntegerField(default=0)
	def __str__(self):
    		return self.name


class Availability(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	day = models.DateField('availability for day')
	shift1 = models.BooleanField(default=False)
	shift2 = models.BooleanField(default=False)
	shift3 = models.BooleanField(default=False)
    #def __str__(self):
    #    return self.day
    #@register.filter
    #def get_item(dictionary, key):
    #    return dictionary.get(key)

class Dayschedule(models.Model):
	day = models.DateField('schedule for day')
	shift = models.IntegerField(default = 0)
	employee = models.IntegerField(default = 0)
	#def __str__(self):
	#	return str(self.employee)