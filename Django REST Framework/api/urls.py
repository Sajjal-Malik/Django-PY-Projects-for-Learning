from django.urls import path
from home.views import index, person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI

from rest_framework.routers import DefaultRouter # type: ignore
router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls


urlpatterns = [
    path('index', index, name="index"),
    path('person', person, name="person"),
    path('login', login, name="login"),
    path('loginapi', LoginAPI.as_view(), name="loginapi"),
    path('register', RegisterAPI.as_view(), name="register"),
    path('personapi', PersonAPI.as_view(), name="personapi"),
]
