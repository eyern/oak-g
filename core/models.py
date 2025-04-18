from django.db import models
from django.utils.html import mark_safe
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from shortuuid.django_fields import ShortUUIDField

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

STATUS_CHOICE = (
	("process", "Processing"),
	("shipped", "Shipped"),
	("delivered", "Delivered"),
)

STATUS = (
	("draft", "Draft"),
	("disabled", "Disabled"),
	("rejected", "Rejected"),
	("in_review", "In Review"),
	("published", "Published"),
)

RATING = (
	( 1, "★☆☆☆☆"),
	( 2, "★★☆☆☆"),
	( 3, "★★★☆☆"),
	( 4, "★★★★☆"),
	( 5, "★★★★★"),
)

def user_directory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
	cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='cat', alphabet='abcdefgh12345')
	title = models.CharField(max_length=100, default="Category Name")
	image = models.ImageField(upload_to='category', default="category.jpg")

	class Meta:
		verbose_name_plural = 'Categories'

	def category_image(self):
		return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

	def __str__(self):
		return self.title

class Tags(models.Model):
	pass

class Vendor(models.Model):
	vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='ven', alphabet='abcdefgh12345')
	
	title = models.CharField(max_length=100, default="Vendor Name")
	image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
	description = RichTextUploadingField(null=True, blank=True, default="Vendor Description")

	address = models.CharField(max_length=100, default="123 Main Street")
	contact = models.CharField(max_length=100, default="+254...")
	email = models.CharField(max_length=100, default="example@mail.com")

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Vendors'

	def vendor_image(self):
		return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

	def __str__(self):
		return self.title

class Product(models.Model):
	pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet='abcdefgh12345')

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
	vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")

	title = models.CharField(max_length=100, default="Product Name")
	image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
	description = RichTextUploadingField(null=True, blank=True, default="Product Description")

	price = models.DecimalField(max_digits=1000, decimal_places=2, default="1.99")
	old_price = models.DecimalField(max_digits=1000, decimal_places=2, default="2.99")

	stock_count = models.PositiveIntegerField(default=10, null=True, blank=True)
	shipping = models.CharField(max_length=100, default="1", null=True, blank=True)

	tags = TaggableManager(blank=True)
	# tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

	product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

	status = models.BooleanField(default=True)
	in_stock = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	digital = models.BooleanField(default=False)

	sku = ShortUUIDField(unique=True, length=4, max_length=30, prefix="sku", alphabet='1234567890')

	date = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Products'

	def product_image(self):
		return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))

	def __str__(self):
		return self.title

	def get_percentage(self):
		new_price = ((self.old_price - self.price) / self.old_price) * 100
		return new_price

class ProductImages(models.Model):
	images = models.ImageField(upload_to="product-images", default="product.jpg")
	product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Product Images'

# Shipping Address
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City / Town")
    state = models.CharField(max_length=150, verbose_name="Phone Number")

    def __str__(self):
        return self.locality

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )



####### Product Review, Wishlist, Address #######



class ProductReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
	review = models.TextField()
	rating = models.IntegerField(choices=RATING, default=None)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Reviews'

	def __str__(self):
		return self.product.title

	def get_rating(self):
		return self.rating

class Wishlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Wishlists'

	def __str__(self):
		return self.product.title

####### Contact, Profile #######



class ContactUs(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	message = models.TextField()

	class Meta:
		verbose_name = 'Contact Us'
		verbose_name_plural = 'Contact Us'

	def __str__(self):
		return self.name
