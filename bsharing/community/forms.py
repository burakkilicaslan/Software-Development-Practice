from django import forms
from .models import community_header, post_type_header
from django.contrib.auth.models import User


class post_type_create_form():
    class Meta: 
        model = post_type_header

        fields = ["name", "desc", "semantic_tag", "fields"]