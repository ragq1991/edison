from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='Index'),
    path('ProvidingOptions', ProvidingOptions.as_view(), name='ProvidingOptions'),
    path('UserSetNumber', UserSetNumber.as_view(), name='UserSetNumber'),
    path('Results', Results.as_view(), name='Results'),
]