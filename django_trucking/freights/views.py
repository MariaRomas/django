from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Freight, Category, Worker, Type
from .forms import ReviewForm
from django.db.models import Q


class TypeYear:
    """Типы и года выхода фильмов"""
    def get_types(self):
        return Type.objects.all()

    def get_years(self):
        return Freight.objects.filter(draft=False).values("year")

class FreightsView(TypeYear, ListView):
    """Список грузов"""
    model = Freight
    queryset = Freight.objects.filter(draft=False)

   
    

class FreightDetailView(TypeYear, DetailView):
    """Полное описание грузоперевозки"""
    model = Freight
    slug_field = "url"
    
class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        freight = Freight.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
                form.freight = freight
                form.save()
                return redirect(freight.get_absolute_url())

class WorkerView(TypeYear, DetailView):
    """Вывод информации о работнике"""
    model = Worker
    template_name = 'freights/worker.html'
    slug_field = "name"

class FilterFreightsView(TypeYear, ListView):
    """Фильтр фильмов"""
    def get_queryset(self):
        queryset = Freight.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(types__in=self.request.GET.getlist("type"))
        )
        return queryset