from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register,name="register"),
    path('me/',views.current_user,name="current_user"),

]
