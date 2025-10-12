from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import (RegisterView, LoginView,
                    register_page, login_page, main_page, UserProfileDetailView, ReviewCreateView, profile_page,
                    logout_view, CurrentUserView)


router = DefaultRouter()
router.register(r'api', views.GuideViewSet)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/me/", CurrentUserView.as_view(), name="current_user"),
    path("logout/", logout_view, name="logout_page"),

    path("", main_page, name="main_page"),
    path("register-page/", register_page, name="register_page"),
    path("login-page/", login_page, name="login_page"),
    path("api/profile/<str:username>/", UserProfileDetailView.as_view(), name="profile-detail"),
    path("api/profile/reviews/create/", ReviewCreateView.as_view(), name="review-create"),
    path('api/profile/<str:username>/guides/', views.profile_guides_api, name='profile_guides_api'),
    path("users/<str:username>/", profile_page, name="profile_page"),

    path('guides/', views.guides_list, name='guides_list'),
    path('search/', views.guides_search, name='guides_search'),
    path('create_guide/', views.create_guide, name='create_guide'),
    path('guides/', include(router.urls)),
]
