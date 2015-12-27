"""tourme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tourme.apps.tourme_app.views.index', name='index'),
    url(r'^vote$', 'tourme.apps.tourme_app.views.vote', name='vote'),
    url(r'^new_game$', 'tourme.apps.tourme_app.views.new_game', name='new_game'),
    url(r'^mission$', 'tourme.apps.tourme_app.views.mission', name='mission'),
    url(r'^choose_players$', 'tourme.apps.tourme_app.views.choose_players', name='choose_players'),
    url(r'^refresh$', 'tourme.apps.tourme_app.views.refresh', name='refresh'),
]
