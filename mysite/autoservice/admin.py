from django.contrib import admin
from .models import Service, Car, Order, OrderLine

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'quantity', 'line_sum']
    readonly_fields = ['line_sum']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'deadline', 'deadline', 'is_overdue', 'total', 'status']
    inlines = [OrderLineInLine]
    readonly_fields = ['date', 'total']

    fieldsets = [
        ('General', {'fields': ('car', 'date', 'deadline', 'client', 'status', 'total')}),
    ]


class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'license_plate', 'vin_code', 'client_name']
    list_filter = ['client_name', 'make', 'model']
    search_fields = ['license_plate', 'vin_code']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
