from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Enum(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.name

class Subject(Enum):
	pass

class Standard(Enum):
	pass


class Syllabus(models.Model):
	subject = models.ForeignKey(Subject, related_name='syllabus')
	standard = models.ForeignKey(Standard, related_name='syllabus')

	class Meta:
		unique_together = ('subject', 'standard',)

	def __str__(self):
		return  self.standard.name + '-' + self.subject.name

class Content(models.Model):
	name = models.CharField(max_length=180)
	body = models.TextField()
	syllabus = models.ManyToManyField(Syllabus, related_name='contents')

	def __str__(self):
		return self.name

class ContentTree(MPTTModel):
	content = models.OneToOneField(Content, related_name='content_tree')
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

	class MPTTMeta:
		order_insertion_by = []

	def __str__(self):
		return self.content.name	
