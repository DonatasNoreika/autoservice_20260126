from django.shortcuts import render
from .models import Service, Car, Order

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

