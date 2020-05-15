from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register , name='register'),
    path('register/', views.register , name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html') ,name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/register.html') ,name='logout'),
    path('login/profile/', views.profile , name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html') ,name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html') ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view() ,name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view() ,name='password_reset_complete'),
    path('findfriend/', views.findfriend , name='findfriend'),
    path('notification/', views.notification , name='notification'),
    path('profilehome/',views.profilehome , name='profilehome'),
    url(r'^profilehome/(?P<pk>\d+)/$',views.profilehome , name='profilehomewithpk'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$',views.change_friends , name='change_friends'),
    path('deletepost/<pk>',views.deletepost , name='deletepost'),
    path('commentpost/<pk>',views.commentpost , name='commentpost'),
    path('showcomment/<pk>',views.showcomment , name='showcomment'),
    path('info/',views.info , name='info'),



]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)