"""
URL configuration for first_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from conputer import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.component_list, name='home'),
    path('builds/', views.build_list, name='build_list'),
    path('building/', views.building, name='building'),
    path('login/', auth_views.LoginView.as_view(template_name='conputer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mybuilds/', views.mybuilds, name='mybuilds'),  
    path('toggle-publish/<int:build_id>/', views.toggle_publish, name='toggle_publish'),
    path('delete-build/<int:build_id>/', views.delete_build, name='delete_build'),
    path('edit/<int:build_id>/', views.edit_build, name='edit_build'),
    path('mybuilds/', views.mybuilds, name='mybuilds'),  
    path('orders/', views.orders_view, name='orders_view'),
    path('checkout/<int:order_id>/', views.checkout_order, name='checkout_order'),
    path('add-to-cart/<int:build_id>/', views.add_to_cart, name='add_to_cart'),
]

if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)