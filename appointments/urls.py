from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorViewSet, LoginView, ReviewListCreateView, ReviewDetailView, AppointmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('doctors/<int:doctor_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('doctors/<int:doctor_id>/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
