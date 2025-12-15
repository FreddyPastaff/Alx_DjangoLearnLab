from django import forms
from django.contrib.auth.models import User
from .models import Post, Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)   
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture'] 

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile  
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)   
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user  

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        return post