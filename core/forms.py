from django import forms
from core.models import ProductReview, Address

class ProductReviewFrom(forms.ModelForm):
	review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write review', \
		'style': 'width: 100%; border: none; background: #f5f5f5; \
		padding: 5px 10px; height: 100px; border-radius: 5px 5px 0px 0px; \
		border-bottom: 2px solid #7fad39; transition: all 0.5s; margin-top: 15px; \
		margin-bottom: 15px;'}))

	class Meta:
		model = ProductReview
		fields = ['review', 'rating']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state']
        widgets = {'locality':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Popular Places Nearby like Restaurants, etc.'}), 'city':forms.TextInput(attrs={'class':'form-control', 'placeholder':'City / Town'}), 'state':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'})}