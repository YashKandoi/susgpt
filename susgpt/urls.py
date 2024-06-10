"""susgpt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from susgpt import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',views.home, name='home'),
    path('admin/', admin.site.urls),
    path('websites/', views.Website_List, name='website-list'),
    path('websites/<str:company_name>/', views.Website_Detail, name='website-detail'), 
    path('susgpt/matchmaking/', views.matchmaking_view, name='matchmaking_view'),
    path('susgpt/discovery/', views.discovery_view, name='discovery_view'),
    path('susgpt/initializeKnowledgeRepo/', views.initialize_knowledgeRepo_view, name='initialize_knowledgeRepo_view'),
    path('susgpt/knowledgeRepoChatbot/', views.knowledgeRepoChatbot_view, name='knowledgeRepoChatbot_view'),
    path('susgpt/clearPdfFolder/', views.clear_folder, name='clearPdfFolder_view')
]

urlpatterns = format_suffix_patterns(urlpatterns)