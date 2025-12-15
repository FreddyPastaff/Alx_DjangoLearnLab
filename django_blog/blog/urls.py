from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # mount authentication routes at root
    # path('', include('your_blog_app.urls')),  # add your blog routes here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from blog.views import UserLoginView, UserLogoutView, register, profile