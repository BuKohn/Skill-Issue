from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import GuideRateAPIView, ReviewCreateView, create_announcement_view, announcement_list_view, \
    ReviewUpdateView, ReviewDeleteView

router = DefaultRouter()
router.register(r'guides', views.GuideViewSet, basename='guides')
router.register(r'announcements', views.AnnouncementViewSet, basename='announcements')

urlpatterns = [
    # --- API endpoints ---
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path("api/login/", views.LoginView.as_view(), name="login"),
    path("api/me/", views.CurrentUserView.as_view(), name="current_user"),
    path("logout/", views.logout_view, name="logout_page"),

    # --- Основные страницы ---
    path("", views.main_page, name="main_page"),
    path("register-page/", views.register_page, name="register_page"),
    path("login-page/", views.login_page, name="login_page"),

    # --- Профили ---
    path("users/edit/", views.profile_edit, name='profile_edit'),
    path("users/<str:username>/", views.profile_page, name="profile_page"),

    # --- API для профилей ---
    path("api/profile/<str:username>/", views.UserProfileDetailView.as_view(), name="profile-detail"),
    path("api/profile/reviews/create/", views.ReviewCreateView.as_view(), name="review-create"),
    path('api/profile/<str:username>/guides/', views.profile_guides_api, name='profile_guides_api'),

    path('api/guides/<int:guide_id>/rate/', GuideRateAPIView.as_view(), name='guide-rate'),
    path('api/reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('api/reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('api/reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),


    # --- Руководства ---
    path('guides/', views.guides_list, name='guides_list'),
    path('search/', views.guides_search, name='guides_search'),
    path('create_guide/', views.create_guide, name='create_guide'),
    path("guides/<int:pk>/", views.guide_detail, name="guide_detail"),

    # --- Объявления ---
    path('create/', create_announcement_view, name='create'),
    path("announcements/", announcement_list_view, name="announcements_list"),

    # --- DRF Router ---
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
