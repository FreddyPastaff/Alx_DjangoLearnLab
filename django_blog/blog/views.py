from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileForm, PostForm
from .models import Post
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

from .forms import RegistrationForm, ProfileForm

class UserLoginView(LoginView):
    template_name = 'blog/login.html'

class UserLogoutView(LogoutView):
    template_name = 'blog/logout.html'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    if request. method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else: 
            messages.error(request, 'please correct the error below.')
    else:
        form = ProfileForm(instance=profile)
        return