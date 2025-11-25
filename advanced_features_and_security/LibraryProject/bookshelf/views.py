from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.contrib import messages
from .forms import ExampleForm

def example_form_view(request):
    form = ExampleForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data.get("description", "")
            messages.success(request, "Form submitted successfully.")
            return redirect("example-form")
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, "form_example.html", {"form": form})

def book_list_view(request):
    books = [{"title": "Django for Beginners"}, {"title": "Two Scoops of Django"}]
    return render(request, "book_list.html", {"books": books})

@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})