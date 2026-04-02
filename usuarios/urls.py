from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # ── Vistas web ────────────────────────────────────────────
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # ── API REST + JWT ────────────────────────────────────────
    path('api/register/',      views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/',         views.LoginAPIView.as_view(),    name='api_login'),
    path('api/logout/',        views.LogoutAPIView.as_view(),   name='api_logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(),      name='api_token_refresh'),
    path('api/profile/',       views.ProfileAPIView.as_view(),  name='api_profile'),
]
