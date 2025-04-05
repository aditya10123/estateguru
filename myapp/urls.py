
 
from django.urls import path,include
from .import views
from .views import PostListView,PostCreateView,PostUpdateView
urlpatterns = [
 
    path('',views.show ,name="home"),

    path('property_cat/<int:id>/',views.properties_view , name="property_cat"),
    path('visitpro/<int:id>/',views.visitpro , name="visitpro"),
    path('propertyform/',views.propertyview),

    path('remove_property/<int:id>/',views.remove_property,name='remove_property'),
     path('remove_rentproperty/<int:id>/',views.remove_rentproperty,name='remove_rentproperty'),


    path('bookproperty/<pid>/',views.bookproperty,name='bookproperty'),
    path('viewproperty/',views.viewproperty,name='viewproperty'),
  
    path('viewrentproperty/',views.viewrentproperty,name='viewrentproperty'),
    path('rent_propertydetails/<int:id>/',views.rent_propertydetails,name='rent_propertydetails'),
    path('register/',views.register,name='register'),
    # path('login/',views.user_login.as_view(),name='login'),
    path('login/',views.logindetails,name='login'),
    path('logout1/',views.logoutdetails,name='logout1'),
    path('propertydetailsform/',views.propertydetails, name="propertydetailsform" ),
    path('rentpropertydetails/',views.rentpropertydetails, name="rentpropertydetails" ),
    path('searchproperty/',views.searchproperty,name='searchproperty'),
    path('updateproperty/<int:qv>/<cid>',views.updateproperty,name='updateproperty'),
    #path('payment/',views.paymentproperty,name='payment'),
    path('rent_property/',views.rent_property,name='rent_property'),
    path('buy_property/',views.buy_property,name='buy_property'),
    
    
    path('contactus/',views.contactus_form,name='contactus'),
    path('checkout/',views.checkoutview,name='checkout'),
    path('checkout1/',views.checkoutview1,name='checkout1'),

    path('payment/success/', views.paymentsuccess, name='paymentsuccess'),
    path('payment/failed/', views.paymentfailed, name='paymentfailed'),

     path('setcookie/',views.set_cookie),
     path('getcookie/',views.get_cookie),
     path('bookrentproperty/<int:pid>/',views.bookrentproperty,name='bookrentproperty'),
    
     path('show_property/',PostUpdateView.as_view(),name='showlist'),
     path('drf_crud/',views.crud_api.as_view(),name="crud"),
     path('forget_password/',views.forget_password,name='forget_password'),
     path('reset_password/<uidb64>/<token>/',views.reset_password,name='resetpassword'),
     path('password_reset_done/',views.password_reset_done,name='passwordresetdone'),
     path('feedback/', views.feedback_view, name='feedback_form'),
     path('thank-you/', views.thank_you, name='thank_you'),
]