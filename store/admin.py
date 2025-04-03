from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','slug','price','stock','category','modified_date','is_available')
    prepopulated_fields= {'slug': ('product_name',)}
    search_fields = ('product_name','Vendor__vendor_name',' Category_name','price')
    list_filter = ('is_available',)


admin.site.register(Product,ProductAdmin)
