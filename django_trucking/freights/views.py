from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Freight, Category
from .forms import ReviewForm
class FreightsView(ListView):
    """Список грузов"""
    model = Freight
    queryset = Freight.objects.filter(draft=False)

   
    

class FreightDetailView(DetailView):
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