from django.urls import path
from . import views
from .views import rentdrone
from .views import logout_view
from .views import delete_order


urlpatterns = [
    path("",views.home, name='home'),
    path('loginpage/', views.loginpage, name='login'),
    path('registerpage/', views.registerpage, name='register'),
    path("adminpanel",views.adminpanel, name='adminpanel'),
    path("rentalrecords",views.rentalrecords, name='rentalrecords'),
    path("ihalist",views.ihalist, name='ihalist'),
    path('ihaedit/<int:drone_id>/', views.ihaedit, name='ihaedit'),
    path('ihaedit/<int:drone_id>/save/', views.ihaedit_save, name='ihaedit_save'),
    path('ihadelete/<int:drone_id>/', views.ihadelete, name='ihadelete'),
    path('ihaadd', views.ihaadd, name='ihaadd'), 
    path('listforuser',views.listforuser, name='listforuser'),
    path('searchresult', views.searchresults, name='searchresult'),
    path('logout/', logout_view, name='logout'),
    path('rentdrone/<int:drone_id>/', rentdrone, name='rentdrone'),
    path('renteddrones/', views.rented_drone_page, name='renteddrones'),
    path('order/<int:order_id>/delete/', delete_order, name='delete_order'),
]