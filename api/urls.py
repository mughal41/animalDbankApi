from django.urls import path
from .views import AnimalDetailsView, CreateAnimalView


urlpatterns = [
       path('animal/', AnimalDetailsView.as_view(), name='fetch-animal-details'),
       path('animal/create/', CreateAnimalView.as_view(), name='bulk-create-animal'),
]
