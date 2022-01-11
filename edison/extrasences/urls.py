from django.urls import path
from .views import *

urlpatterns = [
    path('start', Start.as_view(), name='start'),
    path('step_1', Step1.as_view(), name='step_1'),
    path('step_2', Step2.as_view(), name='step_2'),
    path('finish', Finish.as_view(), name='finish'),
]