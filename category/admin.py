from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Category_name',)}
    list_display = ('Category_name', 'slug','Vendor','updated_at')
    search_fields = ('Category_name','Vendor__vendor_name')

admin.site.register(Category, CategoryAdmin)
