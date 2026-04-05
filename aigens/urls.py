from django.urls import path, re_path
from . import views

app_name = 'aigens'

urlpatterns = [
    path('', views.campaign_generator_view, name='campaign_generator_view'), 
    path('image-video', views.generate_prompt_view, name='generate_prompt_view'), 
    path('marketing-menu', views.marketing_menu, name='marketing_menu'), 
    
]