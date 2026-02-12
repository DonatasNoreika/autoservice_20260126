from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.shortcuts import render, reverse
from django.views.generic.edit import FormMixin
from .models import (Service,
                     Car,
                     Order,
                     CustomUser,
                     OrderLine)
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import (OrderCommentForm,
                    CustomUserCreateForm,
                    OrderCreateUpdateForm)


# from django.contrib.auth.forms import UserCreationForm


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
    paginator = Paginator(cars, per_page=12)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, template_name="cars.html", context={"cars": paged_cars})


def car(request, car_pk):
    return render(request, template_name="car.html", context={"car": Car.objects.get(pk=car_pk)})


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


class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = "profile.html"
    success_url = reverse_lazy('profile')
    fields = ['first_name', 'last_name', 'email', 'photo']

    def get_object(self, queryset=...):
        return self.request.user


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "userorders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 3


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    template_name = "order_form.html"
    # fields = ['car', 'deadline', 'status']
    form_class = OrderCreateUpdateForm
    success_url = reverse_lazy('userorders')

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.save()
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    template_name = "order_form.html"
    # fields = ['car', 'deadline', 'status']
    form_class = OrderCreateUpdateForm

    # success_url = reverse_lazy('userorders')

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().client == self.request.user


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = "order_delete.html"
    context_object_name = "order"
    success_url = reverse_lazy('userorders')

    def test_func(self):
        return self.get_object().client == self.request.user


class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    template_name = "orderline_form.html"
    fields = ['service', 'quantity']

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.kwargs["order_pk"]})

    def test_func(self):
        return Order.objects.get(pk=self.kwargs["order_pk"]).client == self.request.user

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs["order_pk"])
        form.save()
        return super().form_valid(form)

class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    template_name = "orderline_form.html"
    fields = ['service', 'quantity']

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.order.pk})

    def test_func(self):
        return Order.objects.get(pk=self.get_object().order.pk).client == self.request.user

class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine
    template_name = "orderline_delete.html"
    context_object_name = "orderline"

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.order.pk})

    def test_func(self):
        return Order.objects.get(pk=self.get_object().order.pk).client == self.request.user
