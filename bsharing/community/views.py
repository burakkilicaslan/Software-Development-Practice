from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from django.shortcuts import render, get_object_or_404, redirect
from .models import community_header, post_type_header
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from .forms import post_type_create_form
import json



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

class Post_Type_Create(CreateView):
    model = post_type_header
    template_name = "post_type_form.html"
    fields = ["post_community", "name", "desc", "semantic_tag", "fields"]


# def create_post_type(request, community_id):
#     form = post_type_create_form(request.POST)
#     #community = get_object_or_404(community_header, pk = community_id)
#     community_id = request.POST.get("community.id")
#     pt = post_type_header()
#     pt.post_community = community_header.objects.get(community_id)
#     pt.name = request.POST.get("", "")
#     pt.desc = request.POST.get("", "")
#     pt.semantic_tag = request.POST.get ("", "")
#     pt.fields = request.POST.get('fieldJson')
#     pt.save()

#     return redirect('community:community_detail')




