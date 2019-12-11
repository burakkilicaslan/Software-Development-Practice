from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from django.shortcuts import render, get_object_or_404, redirect
from .models import community_header, post_type_header
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from .forms import post_type_create_form, post_create_form
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers




class Community_Listview(ListView):
    context_object_name = "all_communities"
    template_name = "index.html"

    def get_queryset(self):
        return community_header.objects.all()

class Community_DetailView(DetailView):
    model = community_header #Hangi objenin ya da model'in detaylarını görmek istediğimizi belirtiyoruz.
    template_name = "community_detail.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['post_type_list'] = post_type_header.objects.all()
        return context


class Post_Type_DetailView(DetailView):
    model = post_type_header
    context_object_name = "post_type"
    template_name = "post_type_detail.html"

    def get_queryset(self):
        return post_type_header.objects.all()


class Community_Create(CreateView):
    model = community_header
    template_name = "community_form.html"
    fields = ["user_name", "name", "desc","semantic_tag"]


@csrf_exempt
def post_type_create(request, community_header_id):

    community = get_object_or_404(community_header, pk=community_header_id)
    if request.method == 'POST':
        form = post_type_create_form(request.POST)
        if form.is_valid():
            post_type = form.save(commit=False)
            post_type.post_community = community
            jsonfields = request.POST.get('fieldJson')
            post_type.fields = jsonfields
            # for i in request.POST.get("table1", ""):
            #     post_type.fields[i] ={
            #     "fieldLabel": request.POST.get("fieldlabel", ""),
            #     "fieldtype": request.POST.get("fieldtype", ""),
            #     "fieldrequire": request.POST.get("fieldrequire", "")         
            #    }
            post_type.save()

            return HttpResponse("success")
        return render(request, 'post_type_form.html', {'form': form})

    else: 
        form = post_type_create_form()

    return render(request, 'post_type_form.html', {'form': form})
def post_create(request, post_type_id):
    post_type = get_object_or_404(post_type_header, pk=post_type_id)
    form = post_create_form(request.POST)
    tmpObj = serializers.serialize("json", post_type_header.objects.filter(pk=post_type_id).only("datafields"))
    data_fields = json.loads(tmpObj)
    print(data_fields)
    

    # if request.method == 'POST':
    #     form = post_create_form(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.save()

    #         return HttpResponse("success")
    #return render(request, 'post_form.html', {'form': form, "data_fields": data_fields[0]["fields"]["datafields"]})
    return render(request, 'post_form.html', {'form': form, "data_fields": data_fields[0]["fields"]["datafields"][2]})

    
    # else: 
    #     form = post_create_form()
    
    # return render(request, 'post_form.html', {'form': form})









