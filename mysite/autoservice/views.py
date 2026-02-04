from django.shortcuts import render
from .models import Service, Car, Order
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {
        "services": Service.objects.count(),
        "cars": Car.objects.count(),
        "orders_done": Order.objects.filter(status="o").count()
    }
    return render(request, template_name="index.html", context=context)


def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, per_page=3)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, template_name="cars.html", context={"cars": paged_cars})


def car(request, car_pk):
    return render(request, template_name="car.html", context={"car": Car.objects.get(pk=car_pk)})


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 3

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"