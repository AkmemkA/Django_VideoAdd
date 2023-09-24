from django.shortcuts import render
from django.views.generic import TemplateView


class StaticPage(TemplateView):
    template_name = 'index.html'
