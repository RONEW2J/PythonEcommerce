from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'display_is_featured')
    actions = ['mark_as_featured']
    change_list_template = "admin/store/product_change_list.html" 

    def display_is_featured(self, obj):
        featured = getattr(obj, 'is_featured', False)
        return format_html('<span style="color: {};">{}</span>',
                           'green' if featured else 'red',
                           'Yes' if featured else 'No')
    display_is_featured.short_description = 'Featured Status'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} products marked as featured")
    mark_as_featured.short_description = "Mark selected products as Featured"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-report/', self.admin_site.admin_view(self.custom_report_view), name="product-custom-report"),
        ]
        return custom_urls + urls
    
    def custom_report_view(self, request):
        queryset = Product.objects.filter(is_featured=True)
        context = dict(
            self.admin_site.each_context(request),
            products=queryset,
        )
        return TemplateResponse(request, "admin/store/custom_report.html", context)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
