from django.shortcuts import render

# Create your views here.

from .models import * 
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q 
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

def index(request): 
    
    num_prots = Target.objects.all().count() 
    num_LigandInstance = LigandInstance.objects.count() 

    context = {
            'num_targets':num_prots,
            'num_ligands':num_LigandInstance,
            }
    return render(request, 'index.html', context=context)

def help(request):
    return render(request, 'help.html')
def searchhome(request):
    return render(request, 'searchhome.html')

def stats(request):
    return render(request, 'statistics.html')
def bulkdownload(request):
    return render(request, 'bulkdownload.html')

def helpdock(request):
    return render(request, 'helpdock.html')
def helpfind(request):
    return render(request, 'helpfind.html')
def helpresult(request):
    return render(request, 'helpresult.html')
    
import os 
def tool_download(request): 
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path): 
        with open(file_path, 'rb') as f: 
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename='+os.path.basename(file_path)
                return response 

class SearchResultsView(generic.ListView): 
    model = Target
    template_name = 'search_results.html'
    def get_queryset(self): 
        query = self.request.GET.get("q").strip(' ') 
        if query.casefold() == 'gpcr'.casefold(): 
            query = 'GP'
        if query.casefold() == 'protease'.casefold():
            query = 'PR'
        if query.casefold() == 'kinase'.casefold():
            query = 'KI'
        if query.casefold() == 'ion channel'.casefold(): 
            query = 'IC'
        if query.casefold() == 'ionchannel'.casefold(): 
            query = 'IC'
        if query.casefold() == 'nhr'.casefold(): 
            query = 'NHR'
        if query.casefold() == 'hormone receptor'.casefold(): 
            query = 'NHR'
        if query.casefold() == 'nuclear hormone receptor'.casefold(): 
            query = 'NHR'
        object_list = Target.objects.filter(Q(uniprot__icontains=query) | Q(proteintype__icontains=query) |
                Q(protname__icontains=query))
        if len(object_list) == 0:
            object_list = [query.upper()]
        return object_list
            

class ProteinListView(generic.ListView):
    model = Target
    context_object_name = 'target_list'
    template_name = 'database/target_list.html'
    paginate_by = 20


class ProteinDetailView(generic.DetailView): 
    model = Target

class DomainListView(generic.ListView):
    model = Domain
    context_object_name = 'domain_list'
    paginate_by = 20

class DomainDetailView(generic.DetailView): 
    model = Domain
    #template_name = 'database/domain_detail_molstar.html'

class LigandDetailView(generic.DetailView): 
    model = LigandInstance
    template_name = 'database/molstar_practice.html'

class GPCRListView(generic.ListView): 
    model = Target
    template_name = 'database/gpcr.html'
    paginate_by = 20
    def get_queryset(self): 
        return Target.objects.filter(proteintype__exact='GP')

class ProteaseListView(generic.ListView): 
    model = Target
    template_name = 'database/protease.html'
    paginate_by = 20
    def get_queryset(self): 
        return Target.objects.filter(proteintype__exact='PR')

class KinaseListView(generic.ListView): 
    model = Target
    template_name = 'database/kinase.html'
    paginate_by = 20
    def get_queryset(self): 
        return Target.objects.filter(proteintype__exact='KI')

class NHRListView(generic.ListView): 
    model = Target
    template_name = 'database/nhr.html'
    paginate_by = 20
    def get_queryset(self): 
        return Target.objects.filter(proteintype__exact='NHR')

class ICListView(generic.ListView): 
    model = Target
    template_name = 'database/ionchannel.html'
    paginate_by = 20
    def get_queryset(self): 
        return Target.objects.filter(proteintype__exact='IC')

