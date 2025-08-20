from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('help', views.help, name='help'),
        path('statistics', views.stats, name='statistics'),
        path('search_results', views.SearchResultsView.as_view(), name='search_results'),
        path('datadownload', views.bulkdownload, name='bulkdownload'),
        path('search', views.searchhome, name='searchhome'),
        path('targets/', views.ProteinListView.as_view(), name='targets'),
        path('targets/<int:pk>', views.ProteinDetailView.as_view(), name='target-detail'),
        path('domains/<int:pk>', views.DomainDetailView.as_view(), name='domain-detail'),
        path('ligands/<int:pk>', views.LigandDetailView.as_view(), name='ligand-detail'),
        path('gpcrs', views.GPCRListView.as_view(), name='gpcrs'),
        path('proteases',views.ProteaseListView.as_view(), name='proteases'),
        path('kinases',views.KinaseListView.as_view(), name='kinases'),
        path('nhrs',views.NHRListView.as_view(), name='nhrs'),
        path('ionchannels',views.ICListView.as_view(),name='ionchannels'),
        path('download/', views.tool_download, name='tool_download'),
        path('help_dock', views.helpdock, name='helpdock'),
        path('help_find', views.helpfind, name='helpfind'),
        path('help_result', views.helpresult, name='helpresult'),
        ]


