from __future__ import unicode_literals

from django.db import models

import django.utils.timezone as timezone
# Create your models here.

class Codemanagement(models.Model):
	created_time = models.DateTimeField(auto_now_add=True)
	ProjectName = models.CharField(max_length=2000)
	Generated = models.CharField(max_length=2000)
	ReportPeriod = models.CharField(max_length=2000)
	TotalCommits = models.CharField(max_length=2000)
	TotalLinesofCode = models.CharField(max_length=2000)
	Age = models.CharField(max_length=2000)
	TotalFiles = models.CharField(max_length=2000)
	Authors = models.CharField(max_length=2000)
	
	def __unicode__(self):
		return self.ProjectName

class Codestatistical(models.Model):
	created_time = models.DateTimeField(auto_now_add=True)
	Projectname = models.CharField(max_length=2000)
	Allcommits = models.CharField(max_length=2000)
	Allcodelines = models.CharField(max_length=2000)
	Allfiles = models.CharField(max_length=2000)
