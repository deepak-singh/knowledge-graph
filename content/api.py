from tastypie.resources import ModelResource
from content.models import Subject, Standard, Content, Syllabus, ContentTree
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from django.utils.timezone import now
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound
from tastypie import fields
from tastypie.exceptions import BadRequest
from django.db import IntegrityError
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.core.exceptions import ObjectDoesNotExist
from mptt.exceptions import InvalidMove


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

	def dehydrate(self, bundle):
		bundle.data['name'] = bundle.obj.content.name
		return bundle	
		
	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/move_node%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('move_node'), name="api_move_node"),
		]

	# Creation of the tree structure in the begining.	
	def obj_create(self, bundle, **kwargs):
		""" 
			Will be used only for the creation of the tree, 
			if bulk creation will have to change this to use mppt_delay_updates.
			Parse the input and recursively create the tree.
		"""
		def build_tree(data, parent=None):
			for d in data:
				if 'content' in d:
					resource_uri = d['content']
				else:
					resource_uri = d['resource_uri']
				
				content = ContentResource().get_via_uri(resource_uri, bundle.request)
				node = ContentTree.objects.create(content = content, parent=parent)
				
				if 'children' in d:
					build_tree(d['children'], node)
	
		return build_tree(bundle.data)
		 

	def get_child_data(self, obj):
		data = {
			'id': obj.id,
			'content_id': obj.content.id,
			'title': obj.content.name,
			'body': obj.content.body,
		}
		if not obj.is_leaf_node():
			data['children'] = [self.get_child_data(child) for child in obj.get_children()]
		return data

	# Get whole tree making use of cache_tree_children from mptt_tags	
	def get_list(self, request, **kwargs):
		base_bundle = self.build_bundle(request=request)
		objects = self.obj_get_list(bundle=base_bundle, **kwargs)
		sorted_objects = self.apply_sorting(objects, options=request.GET)
		to_be_serialized = {}
		from mptt.templatetags.mptt_tags import cache_tree_children
		objects = cache_tree_children(objects)
		bundles = []
		for obj in objects:
			data = self.get_child_data(obj)
			bundle = self.build_bundle(data=data, obj=obj, request=request)
			bundles.append(self.full_dehydrate(bundle))
			to_be_serialized[self._meta.collection_name] = bundles
			to_be_serialized = self.alter_list_data_to_serialize(request,to_be_serialized)

		return self.create_response(request, to_be_serialized)

	# Move the given node to the given target at a given position	
	def move_node(self, request, **kwargs):
		self.method_check(request, allowed=['patch'])
		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
		target_id = data.get('target_id')
		node_id = data.get('node_id')
		postion = data.get('position')

		try:
			node = ContentTree.objects.get(id=node_id)
			target = ContentTree.objects.get(id=target_id)
			node.move_to(target, postion)

		except ObjectDoesNotExist:
			return self.create_response(request, {
					'success': False,
					'reason': 'Node id or target id not found.',
				}, HttpNotFound )

		except InvalidMove:
			return self.create_response(request, {
					'success': False,
					'reason': 'This move is not allowed',
				}, HttpForbidden )

		return self.create_response(request, {
					'success': True,
					'message': 'Tree updated'
				})	











