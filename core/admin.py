from django.contrib import admin
from core.models import Product, Category, Vendor, Order, OrderItem, \
ProductImages, ProductReview, Wishlist, ShippingAddress, ContactUs

class ProductImagesAdmin(admin.TabularInline):
	model = ProductImages

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductImagesAdmin]
	list_display = ['user', 'title', 'product_image', 'price','category', 'vendor', 'featured', 'product_status', 'pid']

class CategotyAdmin(admin.ModelAdmin):
	list_display = ['title', 'category_image', 'cid']

class VendorAdmin(admin.ModelAdmin):
	list_display = ['title', 'vendor_image', 'vid']

admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0

# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
	model = Order
	readonly_fields = ["date_ordered"]
	fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
	inlines = [OrderItemInline]

class ProductReviewAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'rating']

class WishlistAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'date']

class ShippingAddressAdmin(admin.ModelAdmin):
	list_display = ['user', 'shipping_full_name', 'shipping_email', 'shipping_address1', 'phone_no', 'shipping_city']

class ContactUsAdmin(admin.ModelAdmin):
	list_display = ['name', 'email']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategotyAdmin)
admin.site.register(Vendor, VendorAdmin)
# Unregister Order Model
admin.site.unregister(Order)
# Re-Register our Order AND OrderAdmin
admin.site.register(Order, OrderAdmin)
# Re-Register our Order AND OrderAdmin
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
