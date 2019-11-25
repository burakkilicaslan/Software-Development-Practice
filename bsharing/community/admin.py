from django.contrib import admin
from .models import community_header, define_post_types, post_type_header

admin.site.register(community_header)
admin.site.register(define_post_types)
admin.site.register(post_type_header)
# Register your models here.
