"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from my_project_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('general_stats/', views.general_stats_page, name='general_stats'),
    path('relevance/', views.relevance_page, name='relevance'),
    path('geography/', views.geography_page, name='geography'),
    path('top_skills/', views.top_skills_page, name='top_skills'),
    path('last_vacancies/', views.last_vacancies_page, name='last_vacancies'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
