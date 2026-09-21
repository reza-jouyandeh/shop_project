from django.urls import path
from . import views





urlpatterns = [
    path('start/', views.start_reading, name="start_reading"),
    path('<int:pk>', views.ProductDetailView.as_view(), name="product_detail"),
    path('det/<int:pk>', views.LopDetailView.as_view(), name="product_det"),
]
