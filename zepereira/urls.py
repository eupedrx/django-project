from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, DonationViewSet

router = DefaultRouter()
router.register(r'animals', AnimalViewSet, basename='animal')

# URLs customizadas para donations (ViewSet não-padrão)
donation_list = DonationViewSet.as_view({
    'get': 'list',
})

donation_money_list = DonationViewSet.as_view({
    'get': 'money',
    'post': 'money',
})

donation_money_detail = DonationViewSet.as_view({
    'get': 'money_detail',
    'put': 'money_detail',
    'patch': 'money_detail',
    'delete': 'money_detail',
})

donation_items_list = DonationViewSet.as_view({
    'get': 'items',
    'post': 'items',
})

donation_items_detail = DonationViewSet.as_view({
    'get': 'items_detail',
    'put': 'items_detail',
    'patch': 'items_detail',
    'delete': 'items_detail',
})

urlpatterns = [
    path('', include(router.urls)),
    path('donations/', donation_list, name='donation-list'),
    path('donations/money/', donation_money_list, name='donation-money-list'),
    path('donations/money/<int:pk>/', donation_money_detail, name='donation-money-detail'),
    path('donations/items/', donation_items_list, name='donation-items-list'),
    path('donations/items/<int:pk>/', donation_items_detail, name='donation-items-detail'),
]

