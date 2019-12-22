from django import forms
from .models import community_header, post_type_header, post, community_header, community_join
from django.contrib.auth.models import User



class community_form(forms.ModelForm):
    class Meta:
        model = community_header
        fields = ["name", "desc", "semantic_tag"]

class wikidata_form(forms.ModelForm):
    class Meta:
        model = community_header
        fields = []

class post_type_create_form(forms.ModelForm):
    class Meta: 
        model = post_type_header
        fields = ["name", "desc", "semantic_tag"]

class post_create_form(forms.ModelForm):
    class Meta:
        model = post
        fields = ["name", "desc", "semantic_tag"]

class register_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
         model = User
         fields = ['username', 'email', 'password']

class login_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class community_update_form(forms.ModelForm):
    class Meta:
        model = community_header
        fields = ["name", "desc", "semantic_tag"]

class community_join_form(forms.ModelForm):
    class Meta:
        model = community_join
        fields = []


