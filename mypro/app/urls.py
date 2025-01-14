from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gallery/', views.index, name="index"),
    path('', views.signin, name="signin"),
    path('createuser/', views.usersignup, name="createuser"),
    path('logoutuser/', views.logoutuser, name="logoutuser"),
    path('view_image/<int:pk>/', views.view_image, name="view_image"),
    path('delete_image/<int:pk>/', views.delete_image, name="delete_image"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
