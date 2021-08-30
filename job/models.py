from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Studentuser(models.Model):
	"""docstring for ClassName"""
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	mobile = models.CharField(max_length=100,null=True)
	image = models.FileField(max_length=100)
	gender = models.CharField(max_length=100)
	Type = models.CharField(max_length=100)
	
	def _str_(self)	:
		return self.user.username

class Recruiter(models.Model):
	"""docstring for ClassName"""
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	mobile = models.CharField(max_length=100,null=True)
	image = models.FileField()
	gender = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	Type = models.CharField(max_length=100)
	status = models.CharField(max_length=100)
	
	def _str_(self)	:
		return self.user.username

class Job(models.Model):
	"""docstring for ClassName"""
	recruiter = models.ForeignKey(Recruiter, on_delete = models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()
	title = models.CharField(max_length=100)
	salary = models.FloatField(max_length=100)
	image = models.FileField()
	description = models.CharField(max_length=100)
	experience = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	skills = models.CharField(max_length=100)
	creationdate = models.CharField(max_length=100)
	
	def _str_(self)	:
		return self.title				


class Apply(models.Model):
	"""docstring for ClassName"""
	job = models.ForeignKey(Job, on_delete = models.CASCADE)
	student = models.ForeignKey(Studentuser, on_delete = models.CASCADE)
	resume = models.FileField(null=True)
	apply_date = models.DateField()
	
	
	def _str_(self)	:
		return self.id				

































