from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('asset', views.asset, name="asset"),
    path('workorder/<int:pk>/', views.workorder, name="workorder"),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),
    path('assetview/<int:pk>/', views.assetview, name="assetview"),
    path('assetmainupdate/<int:pk>/', views.assetmainupdate, name="assetmainupdate"),
    path('assetmainlist', views.assetmainlist, name="assetmainlist"),
    path('index', views.index, name="index"),
    path('assetmain', views.assetmain, name="assetmain"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),

]
