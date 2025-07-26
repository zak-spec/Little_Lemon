# from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
import json

from .models import Booking, Menu
from .forms import BookingForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html' 
    
class AboutView(TemplateView):
    template_name = 'about.html'
    

class ReservationListView(View):
    def get(seft,req):
        date=req.GET.get('date',datetime.today().date())
        bookings=Booking.objects.filter(reservation_date=date)
        booking_json=serializers.serialize('json',bookings)
        return render(req, 'bookings.html', {"bookings": booking_json})
    
class BookView(FormView):
    template_name='book.html'
    form_class = BookingForm
    
    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form))
    
class MenuView(TemplateView):
    template_name = 'menu.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = {"menu":Menu.objects.all()} 
        return context
    
class DisplayMenuItemView(TemplateView):
    template_name = 'menu_item.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        context["menu_item"] = get_object_or_404(Menu, pk=pk)
        return context
    
@method_decorator(csrf_exempt,name='dispatch')
class BookingAPI(View):
    def get(self, req):
        data = req.GET.get('date',datetime.today().date())
        bookings = Booking.objects.filter(reservation_date=data)
        bookings_json = serializers.serialize('json', bookings)
        return HttpResponse(bookings_json, content_type='application/json')
    def post(self,req):
        data=json.loads(req.body)
        exist= Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()
        
        if not exist:
            booking=Booking(
                   first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
            return JsonResponse({'success':1})
        else:
            return JsonResponse({'error':1})

