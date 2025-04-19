from django.contrib import admin
from core.models import Product, Category, Vendor, Order, \
ProductImages, ProductReview, Wishlist, Address, ContactUs

class ProductImagesAdmin(admin.TabularInline):
	model = ProductImages

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductImagesAdmin]
	list_display = ['user', 'title', 'product_image', 'price','category', 'vendor', 'featured', 'product_status', 'pid']

class CategotyAdmin(admin.ModelAdmin):
	list_display = ['title', 'category_image', 'cid']

class VendorAdmin(admin.ModelAdmin):
	list_display = ['title', 'vendor_image', 'vid']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')

class ProductReviewAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'rating']

class WishlistAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')

class ContactUsAdmin(admin.ModelAdmin):
	list_display = ['name', 'email']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategotyAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
