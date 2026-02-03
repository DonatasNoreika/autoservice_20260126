from django.shortcuts import render
from .models import Service, Car, Order
from django.views import generic


# Create your views here.
def index(request):
    context = {
        "services": Service.objects.count(),
        "cars": Car.objects.count(),
        "orders_done": Order.objects.filter(status="o").count()
    }
    return render(request, template_name="index.html", context=context)


def cars(request):
    return render(request, template_name="cars.html", context={"cars": Car.objects.all()})


def car(request, car_pk):
    return render(request, template_name="car.html", context={"car": Car.objects.get(pk=car_pk)})


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
