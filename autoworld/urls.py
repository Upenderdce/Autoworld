from django.urls import path
from autoworld import views

urlpatterns = [
    path('', views.scraped_data_view, name='scraped_data_view'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),
    path('compare/', views.compare_cars, name='compare_cars'),
    path('feedback_chart/<str:model_name>/', views.feedback_chart, name='feedback_chart'),
]