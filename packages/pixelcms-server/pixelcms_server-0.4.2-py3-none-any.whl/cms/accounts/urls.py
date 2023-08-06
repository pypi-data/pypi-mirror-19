from django.conf.urls import url

from rest_framework_jwt import views as jwt_views

from . import views


urlpatterns = [
    url(r'^login/$', views.login),
    url(
        r'^social-login-begin/(?P<backend>[0-9a-z\-_]+)/$',
        views.social_login_begin
    ),
    url(r'^social-login-complete/$', views.SocialView.as_view()),
    url(r'^refresh-token/', jwt_views.refresh_jwt_token),
    url(r'^register/$', views.register),
    url(r'^activate/$', views.activate),
    url(r'^resend-activation-message/$', views.resend_activation_message),
    url(r'^send-reset-password-message/$', views.send_reset_password_message),
    url(r'^reset-password/$', views.reset_password),
    url(r'^change-password/', views.change_password),
    url(r'^change-email/', views.change_email),
    url(r'^change-email-confirmation/', views.change_email_confirmation)
]
