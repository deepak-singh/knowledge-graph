from django.contrib import admin
from content.models import Content, Syllabus, Subject, Standard, ContentTree
from mptt.admin import MPTTModelAdmin



admin.site.register(Syllabus)
admin.site.register(Standard)
admin.site.register(ContentTree, MPTTModelAdmin)
admin.site.register(Content)
admin.site.register(Subject)
