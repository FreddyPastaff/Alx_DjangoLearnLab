from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, login_required

"""Registration View"""
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')  # Replace with your desired redirect
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Helper functions to check roles
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Admin-only view
@user_passes_test(is_admin)
@login_required
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


# Librarian-only view
@user_passes_test(is_librarian)
def librarian_view(request):
    """
    View accessible only to users with the 'Librarian' role.
    """
    return render(request, 'relationship_app/librarian_view.html')


# Member-only view
@user_passes_test(is_member)
def member_view(request):
    """
    View accessible only to users with the 'Member' role.
    """
    return render(request, 'relationship_app/member_view.html')

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Required for the check
    return render(request, 'relationship_app/list_books.html', {'books': books})  # Required template path

# Class-based view to show library details and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context
        

