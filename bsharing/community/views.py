from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, View
from django.shortcuts import render, get_object_or_404, redirect
from .models import community_header, post_type_header, post, community_join
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from .forms import post_type_create_form, post_create_form, register_form, login_form, community_form, community_update_form, community_join_form
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
from django.core import serializers
from .serializers import post_type_headerSerializer
from django.utils import timezone
from django.db.models import Q
import requests



def Community_Listview(request):
    if not request.user.is_authenticated:
        all_communities = community_header.objects.order_by("-published_date")
        return render (request, 'index_visitor.html', {'all_communities': all_communities})

    else: 
        all_communities = community_header.objects.order_by("-published_date")
        return render(request, 'index.html', {'all_communities': all_communities}) 
# class Community_Listview(ListView):
#     context_object_name = "all_communities"
#     template_name = "index.html" 
#     def get_queryset(self):
        
#         communities = community_header.objects.order_by("-published_date")
#         return communities
            

class Community_DetailView(DetailView):
    model = community_header #Hangi objenin ya da model'in detaylarını görmek istediğimizi belirtiyoruz.
    template_name = "community_detail.html"
    # def get_queryset(self):
    #     communities = community_header.objects.order_by("-published_date")
    #     return communities
    # Below method enables take post_types for selected communities. However there is simpliest wat to do that. In community detail html with "object.post_type_header_set.all".
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Community_DetailView, self).get_context_data(**kwargs)
        context['post_type_list'] = post_type_header.objects.filter(post_community=self.object).order_by("-published_date")
        return context

class Post_Type_DetailView(DetailView):
    model = post_type_header
    context_object_name = "post_type"
    template_name = "post_type_detail.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Post_Type_DetailView, self).get_context_data(**kwargs)
        context['post_list'] = post.objects.filter(post_posttype=self.object).order_by("-published_date")

        return context

    def get_queryset(self):
        return post_type_header.objects.all()

def Post_Listview(request, post_id):
    post_list = post.objects.get(pk = post_id)
    tmpObj = serializers.serialize("json", post.objects.filter(pk=post_id).only('data_fields'))
    a = json.loads(tmpObj)
    data_fields = json.loads(a[0]["fields"]["data_fields"])
    print(data_fields)
    return render(request, 'post_detail.html', {'post_list': post_list, "data_fields": data_fields})




def Community_Edit(request, community_header_id):
    community = get_object_or_404(community_header, pk=community_header_id)
    object = community_header.objects.get(pk = community_header_id)
    form = community_update_form(instance=object)
    # print(request.user)
    # print(community_header.objects.get(pk = community_header_id).user)
    community_user = community_header.objects.get(pk = community_header_id).user
    if request.user == community_user:
        if request.method == "POST":
            form = community_update_form(request.POST, instance=object)
            #if form.is_valid():
            community = form.save(commit=False)
            community.save()
            #return render ( request, "community_detail.html", {'community_header': community_header})
            return redirect('community:index')
        return render (request, "community_form.html", {'form': form})
    else:
        all_communities = community_header.objects.order_by("-published_date")
        return render (request, "index.html",  {"error_message":"You are not autherizaed to change this community", 'community':community})



def Community_Create(request):
    if not request.user.is_authenticated:
        form = login_form
        return render (request, 'login_form.html', {'form':form}) 

    else:
        if request.method == "POST":
            form = community_form(request.POST)
            if form.is_valid():
                community_header = form.save(commit=False)
                community_header.user = request.user
                community_header.published_date = timezone.now()
                community_header.save()
                return render ( request, "wikidata.html", {'community_header': community_header})
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
            post_type.post_type_user = request.user
            jsonfields = request.POST.get('fieldJson')
            post_type.datafields = jsonfields
            # for i in request.POST.get("table1", ""):
            #     post_type.fields[i] ={
            #     "fieldLabel": request.POST.get("fieldlabel", ""),
            #     "fieldtype": request.POST.get("fieldtype", ""),
            #     "fieldrequire": request.POST.get("fieldrequire", "")         
            #    }
            post_type.save()

            return render (request, 'post_type_detail.html', {'post_type':post_type})
        return render(request, 'post_type_form.html', {'form': form})

    else: 
        form = post_type_create_form()

    return render(request, 'post_type_form.html', {'form': form})

def post_create(request, post_type_id):
    post_type = get_object_or_404(post_type_header, pk=post_type_id)
    tmpObj = serializers.serialize("json", post_type_header.objects.filter(pk=post_type_id).only('datafields'))
    a = json.loads(tmpObj)
    data_fields = json.loads(a[0]["fields"]["datafields"])
    if request.method == 'POST':
        form = post_create_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_posttype = post_type 
            post.post_user = request.user
            jsonfields = request.POST.get('fieldJsonpost')
            post.data_fields = jsonfields
            post.save()
            return render(request, 'post_type_detail.html', {'post_type': post_type})
        return render(request, 'post_form.html', {'form': form})
    else:
        form = post_create_form()

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

    def get(self, request): #this means that IF request.method == 'GET'
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request): #this means that IF request.method == 'POST'
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


class login_user(View):
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

def UserLogout(request):
    logout(request)
    form = login_form(request.POST or None)
    return render(request, "login_form.html", {"form":form})
        

def search(request):
    if not request.user.is_authenticated:
        return render (request, 'index_visitor.html', {}) 
    else: 
        communities=community_header.objects.order_by("-published_date")
        post_types = post_type_header.objects.all()
        posts = post.objects.all()
        query = request.GET.get('q')
        #if request.method == 'POST':
        if query: 
            communities = communities.filter(Q(name__icontains=query) | Q(desc__icontains = query) | Q(semantic_tag__icontains = query)).distinct()
            post_types = post_types.filter(Q(name__icontains = query) | Q(desc__icontains = query) | Q(semantic_tag__icontains = query)).distinct()
            posts = posts.filter(Q(name__icontains=query) | Q(desc__icontains=query) | Q(semantic_tag__icontains = query)).distinct()
            print(communities)
        return render (request, 'search.html', {'communities': communities, 'post_types': post_types, 'posts': posts})
    return render (request, 'index.html', {'communities': communities})

def advanced_search(request):
    #Load all data 
    communities  = community_header.objects.order_by("-published_date")
    post_types  = post_type_header.objects.all() # order by creation date to be added
    posts = post.objects.all()
    message = "You can search only communities, post_types or posts in related field or You can search all of them in navigation search bar."

    #Get items to be searched
    query_community = request.GET.get('q_community')
    query_posttypes = request.GET.get('q_posttypes')
    query_posts = request.GET.get('q_posts')

    #Query Them
    if query_community:
        communities = communities.filter(Q(name__icontains=query_community) | Q(desc__icontains = query_community) | Q(semantic_tag__icontains = query_community)).distinct()

        return render(request, "advanced_search.html", {"communities":communities})

    elif query_community:
        post_types = post_types.filter(Q(name__icontains = query_posttypes) | Q(desc__icontains = query_posttypes) | Q(semantic_tag__icontains = query_posttypes)).distinct()

        return render(request, "advanced_search.html", {"post_types":post_types})

    elif query_posts:
        posts = posts.filter(Q(name__icontains=query_posts) | Q(desc__icontains=query_posts) | Q(semantic_tag__icontains = query_posts)).distinct()

        return render(request, "advanced_search.html", {"post":posts})
    
    else:
        return render(request, "advanced_search.html", {"message":message, "error": "There is no result related to your search"})


def join(request, community_header_id):

    if not request.user.is_authenticated:
        return render (request, 'index_visitor.html', {})
    else:
        all_communities = community_header.objects.order_by("-published_date")
        community = get_object_or_404(community_header, pk=community_header_id)
        form = community_join_form(request.POST or None)
        community_j = form.save(commit=False)

        #control whether user join already or not. 
        control = community_join.objects.filter(joined_user = request.user).filter(related_community = community_header_id)
        print(control)
        if control:
            #print("yok")
            return render(request, 'index.html', {'all_communities': all_communities, 'error_message': "You already joined!"})     
        else:
            #print("var")
            community_j.related_community = community
            community_j.joined_user = request.user
            community_j.save()
            status = "Success, You just joined!"
            return render(request, 'index.html', {'all_communities': all_communities, 'status': status})    
        #all_communities = community_header.objects.order_by("-published_date")

def AddSemanticTag(request):
    tag = [] #Create Empty List
    if request.method == "POST":   
        input_for_tag = request.POST.get("input_box", "Hatali Giris")
        #-----------000-------------------000------------------- 
        #Wikidata Query
        API_ENDPOINT = "https://www.wikidata.org/w/api.php"
        query = input_for_tag
        params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'limit': '3',
        'search': query
        }
        wiki_request = requests.get(API_ENDPOINT, params=params)
        wiki_return = wiki_request.json()["search"] 
        #-----------000-------------------000------------------- 
        #Put Items Into A List For Render
        for i in range(len(wiki_return)):
            try:
                tag.append(wiki_return[i]["description"])
            except KeyError:
                continue
        
        return render(request, "wikidata.html",{"tag":tag})

    return render(request, "wikidata.html",{"tag":tag})





