from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from userauths.models import User
from userauths.forms import UserRegisterForm

from core.forms import AddressForm
from core.models import Address, Order

from django.contrib import messages
from django.utils.decorators import method_decorator # for Class Based Views
from django.views import View

# User = settings.AUTH_USER_MODEL

def register_view(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST or None)

		if form.is_valid():
			new_user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Hey {username}, Your account was created successfully")
			new_user = authenticate(username=form.cleaned_data['email'], 
									password=form.cleaned_data['password1'] 	
				)
			login(request, new_user)

			return redirect("core:index")
	else:
		form = UserRegisterForm()

	context = {
		'form': form
	}

	return render(request, 'userauths/sing-up.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    next_url = request.GET.get('next', None)

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")

                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('core:index')
            else:
                messages.warning(request, "Password is wrong.")
        except User.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist!")

    return render(request, 'userauths/sing-in.html')

def logout_view(request):
	logout(request)
	messages.success(request, "You logged out.")
	return redirect('userauths:sing-in')

@login_required
def account(request):
	if request.method == 'POST':
		
		new_username = request.POST.get('username').replace(" ", "").lower()

		if ' ' in new_username:
			messages.warning(request, "Username cannot contain spaces.")
			return redirect('userauths:account')

		if len(new_username) < 3 or len(new_username) > 12:
			messages.warning(request, 'Username must be between 3 and 12 characters.')
			return redirect('userauths:account')

		if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
			messages.warning(request, f'Username "{new_username}" is already taken!')
			return redirect('userauths:account')

		request.user.username = new_username
		request.user.save()

		new_name = request.POST.get('name')
		new_phone = request.POST.get('phone')
		new_bio = request.POST.get('bio')
		new_image = request.FILES.get('image')

		account = request.user
		account.name = new_name
		account.phone = new_phone
		account.bio = new_bio

		if new_image:
			account.image = new_image
			
		account.save()

		messages.success(request, 'Account updated successfully.')

		return redirect('userauths:account')	

	return render(request, 'userauths/account.html')

@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'core/orders.html', {'orders': all_orders})

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'userauths/account.html', {'addresses':addresses, 'orders':orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'userauths/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('userauths:account')

@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('userauths:account')