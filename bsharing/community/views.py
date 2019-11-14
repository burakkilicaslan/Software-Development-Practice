from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView)
from django.shortcuts import render
from .models import community_header
from django.template import loader


class Community_Listview(ListView):
    context_object_name = "all_communities"
    template_name = "index.html"

    def get_queryset(self):
        return community_header.objects.all()

class Community_DetailView(DetailView):
    model = community_header #Hangi objenin ya da model'in detaylarını görmek istediğimizi belirtiyoruz.
    template_name = "community_detail.html"
    
    def get_queryset(self):
        return community_header.objects.all()

class Community_Create(CreateView):
    model = community_header
    template_name = "community_form.html"
    fields = ["user_name", "name", "desc","semantic_tag"]

