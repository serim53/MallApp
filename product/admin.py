from django.contrib import admin

# Register your models here.
from product.models import Product, Category, Comment

admin.site.register(Product)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)