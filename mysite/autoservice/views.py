from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Service, Car, Order
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "services": Service.objects.count(),
        "cars": Car.objects.count(),
        "orders_done": Order.objects.filter(status="o").count(),
        'num_visits': num_visits,
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

def search(request):
    query = request.GET.get('query')
    context = {
        "query": query,
        "cars": Car.objects.filter(Q(make__icontains=query) |
                                   Q(model__icontains=query) |
                                   Q(license_plate__icontains=query) |
                                   Q(vin_code__icontains=query) |
                                   Q(client_name__icontains=query)),
    }
    return render(request, template_name="search.html", context=context)

class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "userorders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)