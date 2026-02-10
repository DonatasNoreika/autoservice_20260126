from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

# Create your models here.
class Service(models.Model):
    name = models.CharField()
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name = "Paslauga"
    #     verbose_name_plural = "Paslaugos"


class Car(models.Model):
    make = models.CharField()
    model = models.CharField()
    license_plate = models.CharField()
    vin_code = models.CharField()
    client_name = models.CharField()
    photo = models.ImageField(upload_to='cars', null=True, blank=True)
    description = HTMLField(default="")

    def __str__(self):
        return f"{self.make} {self.model}"


class Order(models.Model):
    car = models.ForeignKey(to="Car",
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    client = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS = (
        ('c', "Confirmed"),
        ('i', 'In Progress'),
        ('o', 'Completed'),
        ('e', 'Canceled'),
    )

    status = models.CharField(choices=STATUS, default='c')

    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()

    # def total(self):
    #     result = 0
    #     for line in self.lines.all():
    #         result += line.line_sum()
    #     return result

    def total(self):
        return sum(line.line_sum() for line in self.lines.all())


    def __str__(self):
        return f"{self.car} ({self.date}) - {self.total()}"


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order",
                              on_delete=models.CASCADE,
                              related_name="lines")
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def line_sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service.name} ({self.service.price}) * {self.quantity} = {self.line_sum()}"


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order",
                              on_delete=models.CASCADE,
                              related_name="comments")
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-pk']

