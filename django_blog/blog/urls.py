from django.urls import path
from .views import PostListView,PostDetailView,PostDeleteView,PostCreateView,PostUpdateView, PostByTagListView
from django.contrib.auth import views as auth_views
from . import views
from .views import  CommentUpdateView, CommentDeleteView,CommentCreateView,search_posts, posts_by_tag
 
urlpatterns = [
    # LIST view of posts
    path('post/', PostListView.as_view(), name='post_list'),

    # CREATE a new post
    path('post/new/', PostCreateView.as_view(), name='post_create'),

    # DETAIL view of a post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # UPDATE a post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),

    # Add a new comment to a post   views.CommentCreateView.as_view()  edited to CommentCreateView.as_view()
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
        path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('search/', search_posts, name='search_posts'),
    path('tags/<str:tag>/', posts_by_tag, name='posts_by_tag'),
    path('', PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name='posts_by_tag'),
]