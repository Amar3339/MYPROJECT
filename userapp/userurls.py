from django.urls import path
from . import views

urlpatterns = [

    path('userdash/', views.userdash, name='userdash'),
    path('logout/', views.userlogout, name='userlogout'),

    path('viewcart/', views.viewcart, name='viewcart'),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('removeitem/<int:id>/', views.removeitem, name='removeitem'),

]