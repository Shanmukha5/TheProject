from django.db import models

#for rating it is hard to take decimal values so get the rating multiply it with 100 and store it
class workerdetails(models.Model): 
	profilelink = models.CharField(max_length=1000000, default="Not saved properly")
	name = models.CharField(max_length=100000, default="Not saved properly")
	skill = models.CharField(max_length=1000, default="Not saved properly")
	rating = models.IntegerField(null=True, default="000")
	description = models.CharField(max_length=10000,null=True, default="default")


	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name

	

#diehard


