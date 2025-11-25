from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django import forms  # Assuming you have a form for Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        
        fields = ['title', 'author', 'published_date']

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
# These functions assume that each User has a related 'userprofile' model
# with a 'role' field (e.g., 'Admin', 'Librarian', 'Member').
def is_admin(user):
    userprofile = getattr(user, 'userprofile', None)
    return userprofile is not None and userprofile.role == 'Admin'
def is_librarian(user):
    return getattr(user, 'userprofile', None) and user.userprofile.role == 'Librarian'
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    userprofile = getattr(user, 'userprofile', None)
    return userprofile is not None and userprofile.role == 'Member'

# Admin-only view
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')
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
        

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
