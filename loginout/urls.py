from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('findpassword/', views.findpassword, name="findpassword"),
    path('changepassword/', views.changepassword, name="changepassword"),
]