from tastypie.resources import ModelResource
from content.models import Subject, Standard, Content, Syllabus, ContentTree
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
# from tastypie.serializers import PrettyJSONSerializer
from django.utils.timezone import now
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound
from tastypie import fields
from tastypie.exceptions import BadRequest
from django.db import IntegrityError
from tastypie.constants import ALL, ALL_WITH_RELATIONS


class StandardResource(ModelResource):
	class Meta:
		queryset = Standard.objects.all()
		resource_name = 'standard'
		authorization = Authorization()
		filtering = {
			"id": ALL
		}

class SubjectResource(ModelResource):
	class Meta:
		queryset = Subject.objects.all()
		resource_name = 'subject'
		authorization = Authorization()
		filtering = {
			"id": ALL
		}

class SyllabusResource(ModelResource):
	subject = fields.ForeignKey(SubjectResource, 'subject', full=True)		
	standard = fields.ForeignKey(StandardResource, 'standard', full=True)
	
	class Meta:
		queryset = Syllabus.objects.all()
		resource_name = 'syllabus'
		authorization = Authorization()
		# fields = ["id", "title", "body"]
		filtering = {
			"subject": ALL_WITH_RELATIONS,
			"standard": ALL_WITH_RELATIONS
		}

class ContentResource(ModelResource):
	syllabus = fields.ToManyField(SyllabusResource, 'syllabus', full=False)

	class Meta:
		resource_name = 'content'
		authorization = Authorization()
		queryset = Content.objects.all()
		filtering = {
			"syllabus": ALL_WITH_RELATIONS
		}


class ContentTreeResource(ModelResource):
	children = fields.ToManyField('self', 'children', full=True, null=True)
	content = fields.ToOneField(ContentResource, 'content', full=True, null=True)
	class Meta:
		resource_name = 'content_tree'
		authorization = Authorization()
		queryset = ContentTree.objects.all()
		include_resource_uri = False
		excludes = ['lft', 'rght']
		filtering = {
			"content": ALL_WITH_RELATIONS,
			"children": ALL,
			"level": ALL
		}

	# def get_child_data(self, obj):
	# 	data = {
	# 		'id': obj.id,
	# 		'content_id': obj.content.id,
	# 		'title': obj.content.title,
	# 		'body': obj.content.body,
	# 	}
	# 	if not obj.is_leaf_node():
	# 		data['children'] = [self.get_child_data(child) for child in obj.get_children()]
	# 	return data

	# def get_list(self, request, **kwargs):
	# 	base_bundle = self.build_bundle(request=request)
	# 	objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
	# 	sorted_objects = self.apply_sorting(objects, options=request.GET)
	# 	to_be_serialized = {}
	# 	from mptt.templatetags.mptt_tags import cache_tree_children
	# 	objects = cache_tree_children(objects)
	# 	bundles = []
	# 	for obj in objects:
	# 		data = self.get_child_data(obj)
	# 		bundle = self.build_bundle(data=data, obj=obj, request=request)
	# 		bundles.append(self.full_dehydrate(bundle))
	# 		to_be_serialized[self._meta.collection_name] = bundles
	# 		to_be_serialized = self.alter_list_data_to_serialize(request,to_be_serialized)

	# 	return self.create_response(request, to_be_serialized)






