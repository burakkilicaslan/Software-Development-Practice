from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from django.shortcuts import render, get_object_or_404, redirect
from .models import community_header, post_type_header
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from .forms import post_type_create_form, post_create_form, register_form, login_form, community_form
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from .serializers import post_type_headerSerializer
from django.utils import timezone




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
        context['post_type_list'] = post_type_header.objects.all()
        return context


class Post_Type_DetailView(DetailView):
    model = post_type_header
    context_object_name = "post_type"
    template_name = "post_type_detail.html"

    def get_queryset(self):
        return post_type_header.objects.all()


def Community_Create(request):
    if not request.user.is_authenticated:
        return render (request, 'login.html') 

    else:
        if request.method == "POST":
            form = community_form(request.POST)
            if form.is_valid():
                community_header = form.save(commit=False)
                community_header.user = request.user
                community_header.published_date = timezone.now()
                community_header.save()
                return render ( request, "community_detail.html", {'community_header': community_header})
            return render ( request, "community_form.html", {'community_header': community_header})
        else:
            form = community_form()
            return render ( request, "community_form.html", {"form": form})



@csrf_exempt
def post_type_create(request, community_header_id):

    community = get_object_or_404(community_header, pk=community_header_id)
    if request.method == 'POST':
        form = post_type_create_form(request.POST)
        if form.is_valid():
            post_type = form.save(commit=False)
            post_type.post_community = community
            jsonfields = request.POST.get('fieldJson')
            post_type.datafields = jsonfields
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
    tmpObj = serializers.serialize("json", post_type_header.objects.filter(pk=post_type_id).only('datafields'))
    a = json.loads(tmpObj)
    data_fields = json.loads(a[0]["fields"]["datafields"])
    # if request.method == 'POST':
    #     form = post_create_form(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.save()

    #         return HttpResponse("success")
    #return render(request, 'post_form.html', {'form': form, "data_fields": data_fields[0]["fields"]["datafields"]})
    return render(request, 'post_form.html', {'form': form, 'post_type': post_type, "data_fields": data_fields})

    
    # else: 
    #     form = post_create_form()
    
    # return render(request, 'post_form.html', {'form': form})

#------------------------- ************************ -------------------------------------
# Hem class based yapı ile generic view kullanılabilir, hem de fonksiyon bazlı view ile yazılabilir. Her ikisine de yer vereceğim ancak bir tanesi comment olarak kalacak. 

class register_form(View):
    form_class = register_form
    template_name = "registration_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('community:index')
        return render(request, self.template_name, {'form': form})


class login(View):
    form_class = login_form
    template_name = 'login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('community:index')
            else:
                return render(request, self.template_name,{"error_message":"Your Account Has Been Disabled"})
        else:
            return render(request, self.template_name, {"error_message":"Invalid Login Credentials"})
        return render(request, self.template_name, {'form': form})
        







