from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import *

urlpatterns = [
    
    path("sign-up/", SignUpUser.as_view(), name="sign-up"),
    path("sign-in/", SignInUser.as_view(), name="sign-in"),
    path("log-out/", logout_user, name="log-out"),
    path("profile/<int:user_id>/", ShowProfile.as_view(), name="profile"),
    path("report/<int:report_id>/", ShowReport.as_view(), name="report"),
    path("profile/report/<int:pk>/delete/", DeleteReport.as_view(), name="report-delete"),
    path(
        "reset_password/",
        CustomPasswordResetView.as_view(template_name="password-reset.html"),
        name="password_reset",
    ),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="password-reset-sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(template_name="password-reset-confirm.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"), name="password_reset_complete"),
]
