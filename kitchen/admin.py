from django.contrib import admin
from .models import Category, FoodItem, Cart, Order

admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Cart)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'total',
        'status',
    )

    list_filter = ('status',)

    search_fields = (
        'name',
        'phone',
    )

    list_editable = ('status',)