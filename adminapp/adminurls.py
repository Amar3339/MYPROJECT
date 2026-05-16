from django.urls import path
from . import views
from . import *


urlpatterns=[
    path('admindash/', views.admindash, name='admindash'),
    path('adminlogout/',views.adminlogout, name='adminlogout'),
    path('viewenquiry/',views.viewenquiry, name='viewenquiry'),
    path('adminchangepwd/',views.adminchangepwd, name='adminchangepwd'),
    path('delenquiry/<int:id>',views.delenquiry, name='delenquiry'),
    path('addcat/',views.addcat, name='addcat'),
    path('viewcat/',views.viewcat, name='viewcat'),
    path('addbook/',views.addbook, name='addbook'),
    path('viewbook/',views.viewbook, name='viewbook'),
    path('delcat/<int:id>',views.delcat, name='delcat'),
    path('editcat/<int:id>',views.editcat, name='editcat'),
    path('delbook/<int:id>',views.delbook, name='delbook'),
    path('editbook/<int:id>',views.editbook, name='editbook'),
    
    
    
    
    
]