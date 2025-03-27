from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from checkouts.views import custom_404_view  # ✅ Import your custom 404 view

handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),  # Delegate to products app
    path('accounts/', include('accounts.urls')),
    path('customers/', include('customers.urls')),
    path('orders/', include('orders.urls')),
    path('checkouts/', include('checkouts.urls')),
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
]

urlpatterns += staticfiles_urlpatterns()  
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # gerenciar imagens