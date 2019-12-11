from django import forms
from .models import community_header, post_type_header, post
from django.contrib.auth.models import User


class post_type_create_form(forms.ModelForm):
    class Meta: 
        model = post_type_header
        fields = ["name", "desc", "semantic_tag"]

class post_create_form(forms.ModelForm):
    class Meta:
        model = post
        fields = ["name", "desc", "semantic_tag"]