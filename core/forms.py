from django import forms
from core.models import ProductReview, ShippingAddress

class ProductReviewFrom(forms.ModelForm):
	review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write review', \
		'style': 'width: 100%; border: none; background: #f5f5f5; \
		padding: 5px 10px; height: 100px; border-radius: 5px 5px 0px 0px; \
		border-bottom: 2px solid #7fad39; transition: all 0.5s; margin-top: 15px; \
		margin-bottom: 15px;'}))

	class Meta:
		model = ProductReview
		fields = ['review', 'rating']

class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
	shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)
	shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}), required=True)
	phone_no = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}), required=True)
	shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'phone_no', 'shipping_city']

		exclude = ['user',]