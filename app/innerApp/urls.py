from django.urls import path
from . import views
from django.conf import settings
from .views import ListManipulationViewSet

sumList = ListManipulationViewSet.as_view({
    "post":'list',  
})

urlpatterns = [
path('sumList/', sumList , name= 'sumList'),    

]