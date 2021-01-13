from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .models import Freight, Category, Worker, Type, Rating
from .forms import ReviewForm, RatingForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse


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
    paginate_by = 1

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip  
    

class FreightDetailView(TypeYear, DetailView):
    """Полное описание грузоперевозки"""
    model = Freight
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context
    
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
    paginate_by = 2
    def get_queryset(self):
        queryset = Freight.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(types__in=self.request.GET.getlist("types"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["type"] = ''.join([f"type={x}&" for x in self.request.GET.getlist("type")])
        return context

class JsonFilterFreightsView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Freight.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(types__in=self.request.GET.getlist("type"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"freight": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                freight_id=int(request.POST.get("freight")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Freight.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context