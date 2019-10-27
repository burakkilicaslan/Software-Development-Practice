from django.shortcuts import render
from .models import community_header
from django.template import loader


# Create your views here.

# def index(request): 
#     #return render(request, 'index.html', {'name': 'Burak Kılıçaslan'})   
#     # return HttpResponse("<h2> Details for community</h2>")

#     all_community = community_header.objects.all()
#     context = {
#         'all_community': all_community
#     }
#     return render(request, 'index.html', context)

# def index(request, community_id):

def index(request):
    
    # all_community = community_header.objects.all()
    # community_name = community_header.name
    # community_desc = community_header.desc
    # context = {
    #     'all_community': all_community,
    # }
    # return render(request, 'community.html', context)
    return render(request, 'index.html')