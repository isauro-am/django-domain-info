from django.urls import path, include
from .views import DomainView

urlpatterns = [
    
    path('', DomainView.as_view(), name='DomainView'),

]
